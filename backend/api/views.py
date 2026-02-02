import io
import os
import logging
from .models import Dataset, Equipment, DatasetSummary
from .serializers import (
    DatasetSerializer, 
    DatasetListSerializer, 
    DatasetSummarySerializer, 
    EquipmentSerializer
)
from .services import DatasetService
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


def health_check(request):
    """Health check endpoint for UptimeRobot to keep Render service awake."""
    return JsonResponse({"status": "ok"})

# Report generation imports
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger('api')

def home(request):
    return render(request, "index.html")


from rest_framework.authtoken.models import Token # Import Token

class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated] # Secure view
    
    def post(self, request):
        if "file" not in request.FILES:
            return Response(
                {"error": "No file uploaded"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES["file"]
        if not file.name.endswith(".csv"):
            return Response(
                {"error": "File must be a CSV"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # User is guaranteed to be authenticated now
        user = request.user

        try:
            logger.info(f"Starting processing for file: {file.name}")
            dataset = DatasetService.process_dataset(file, user)
            logger.info(f"Successfully processed dataset: {dataset.id}")
            
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error during CSV processing")
            return Response(
                {"error": "An internal error occurred while processing the file."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for Datasets since creation is handled via UploadCSVView.
    """
    # queryset = Dataset.objects.all().order_by("-created_at") # Removed to use get_queryset
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dataset.objects.filter(uploaded_by=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return DatasetListSerializer
        return DatasetSerializer

    @action(detail=True, methods=["get"])
    def equipment(self, request, pk=None):
        equipment = Equipment.objects.filter(dataset_id=pk)
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        try:
            summary = DatasetSummary.objects.get(dataset_id=pk)
            serializer = DatasetSummarySerializer(summary)
            return Response(serializer.data)
        except DatasetSummary.DoesNotExist:
            return Response(
                {"error": "Summary not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"])
    def report(self, request, pk=None):
        """Generates a PDF report for the dataset."""
        try:
            dataset = self.get_object()
            summary = dataset.summary
            equipment = dataset.equipment.all()
            
            return self._generate_pdf(dataset, summary, equipment)
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_pdf(self, dataset, summary, equipment):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=inch/2, leftMargin=inch/2,
            topMargin=inch/2, bottomMargin=inch/2
        )

        elements = []
        styles = getSampleStyleSheet()
        
        # Styles
        title_style = ParagraphStyle(
            "ReportTitle", 
            parent=styles["Heading1"], 
            fontSize=24, 
            textColor=colors.HexColor("#1a1a2e"),
            alignment=1, 
            spaceAfter=30
        )
        h2_style = ParagraphStyle(
            "ReportH2", 
            parent=styles["Heading2"], 
            fontSize=16, 
            textColor=colors.HexColor("#2d3436"),
            spaceBefore=20, 
            spaceAfter=10
        )

        # Title
        elements.append(Paragraph("Chemical Equipment Analysis Report", title_style))
        elements.append(Paragraph(f"<b>Dataset Name:</b> {dataset.name}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Date Generated:</b> {dataset.created_at.strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
        elements.append(Spacer(1, 20))

        # Summary Table
        elements.append(Paragraph("Executive Summary", h2_style))
        summary_data = [
            ["Metric", "Value", "Metric", "Value"],
            ["Total Equipment", summary.total_count, "Avg Flowrate", f"{summary.avg_flowrate:.2f}"],
            ["Avg Pressure", f"{summary.avg_pressure:.2f}", "Avg Temperature", f"{summary.avg_temperature:.2f}"],
            ["Max Pressure", f"{summary.max_pressure:.2f}", "Max Temperature", f"{summary.max_temperature:.2f}"]
        ]
        
        t = Table(summary_data, colWidths=[2*inch, 1.5*inch, 2*inch, 1.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f2f6")),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#dfe6e9")),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('PADDING', (0,0), (-1,-1), 12),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # Advanced Statistics (Calculated on the fly)
        # Convert queryset/list to DataFrame for easy analysis
        df = pd.DataFrame(list(equipment.values()))
        if not df.empty:
            elements.append(Paragraph("Detailed Statistical Analysis", h2_style))
            
            # Calculate Stats
            stats_data = [["Parameter", "Mean", "Median", "Std Dev", "Min", "Max"]]
            for param in ['flowrate', 'pressure', 'temperature']:
                if param in df.columns:
                    stats_data.append([
                        param.capitalize(),
                        f"{df[param].mean():.2f}",
                        f"{df[param].median():.2f}",
                        f"{df[param].std():.2f}",
                        f"{df[param].min():.2f}",
                        f"{df[param].max():.2f}"
                    ])
            
            t_stats = Table(stats_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            t_stats.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#dfe6e9")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('ALIGN', (1,1), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ]))
            elements.append(t_stats)
            elements.append(Spacer(1, 20))

        # Equipment List (Truncated if too long, or full?)
        # For a report, usually full list is okay unless huge. Let's list top 50 or so?
        # Requirement says "Generate PDF report", implies full report. 
        elements.append(Paragraph("Detailed Equipment List", h2_style))
        
        data_table = [["Name", "Type", "Flowrate", "Pressure", "Temp"]]
        for eq in equipment:  
            data_table.append([
                eq.equipment_name,
                eq.equipment_type,
                f"{eq.flowrate:.2f}",
                f"{eq.pressure:.2f}",
                f"{eq.temperature:.2f}"
            ])
            
        t_data = Table(data_table, repeatRows=1)
        t_data.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2d3436")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 9),
        ]))
        elements.append(t_data)
        elements.append(Spacer(1, 20))

        # Visualizations Section
        elements.append(Paragraph("Visualizations", h2_style))
        
        # 1. Type Distribution Pie Chart
        pie_chart = self._create_pie_chart(summary.type_distribution)
        if pie_chart:
            elements.append(Paragraph("Equipment Type Distribution", styles["Heading3"]))
            elements.append(pie_chart)
            elements.append(Spacer(1, 15))

        # 2. Averages Bar Chart
        bar_chart = self._create_bar_chart(summary)
        if bar_chart:
            elements.append(Paragraph("Average Performance Metrics", styles["Heading3"]))
            elements.append(bar_chart)
            elements.append(Spacer(1, 15))

        # 3. Correlation Heatmap
        corr_heatmap = self._create_correlation_heatmap(df)
        if corr_heatmap:
            elements.append(Paragraph("Parameter Correlation Matrix", styles["Heading3"]))
            elements.append(corr_heatmap)
            elements.append(Spacer(1, 15))

        doc.build(elements)
        buffer.seek(0)
        
        from django.http import HttpResponse
        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{dataset.name}_report.pdf"'
        return response

    def _create_correlation_heatmap(self, df):
        """Generate a correlation heatmap Image flowable"""
        if df.empty:
            return None
        
        try:
            cols = ['flowrate', 'pressure', 'temperature']
            # Ensure columns exist
            cols = [c for c in cols if c in df.columns]
            if len(cols) < 2:
                return None
                
            corr_matrix = df[cols].corr()
            
            plt.figure(figsize=(5, 4))
            plt.imshow(corr_matrix, cmap='coolwarm', interpolation='nearest', vmin=-1, vmax=1)
            plt.colorbar()
            
            # Add labels
            ticks = np.arange(len(cols))
            plt.xticks(ticks, [c.capitalize() for c in cols], rotation=45)
            plt.yticks(ticks, [c.capitalize() for c in cols])
            plt.title('Correlation Matrix')
            
            # Add text annotations
            for i in range(len(cols)):
                for j in range(len(cols)):
                    text = f"{corr_matrix.iloc[i, j]:.2f}"
                    plt.text(j, i, text, ha="center", va="center", color="black")
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            img_buffer.seek(0)
            return Image(img_buffer, width=4*inch, height=3.2*inch)
        except Exception as e:
            logger.error(f"Failed to create heatmap: {e}")
            return None

    def _create_pie_chart(self, distribution):
        """Generate a pie chart Image flowable"""
        if not distribution:
            return None
            
        try:
            plt.figure(figsize=(6, 4))
            labels = list(distribution.keys())
            sizes = list(distribution.values())
            colors = ['#00D9A5', '#FF6B35', '#00A8E8', '#FFD166', '#EF476F', '#8338EC']
            
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)], startangle=90)
            plt.axis('equal')
            plt.title('Equipment Types')
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            img_buffer.seek(0)
            return Image(img_buffer, width=5*inch, height=3.5*inch)
        except Exception as e:
            logger.error(f"Failed to create pie chart: {e}")
            return None

    def _create_bar_chart(self, summary):
        """Generate a bar chart Image flowable"""
        try:
            plt.figure(figsize=(6, 4))
            metrics = ['Avg Flow', 'Avg Pressure', 'Avg Temp']
            values = [summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature]
            colors = ['#00D9A5', '#FF6B35', '#00A8E8']
            
            bars = plt.bar(metrics, values, color=colors)
            plt.ylabel('Values')
            plt.title('Average Metrics')
            plt.grid(axis='y', alpha=0.3)
            
            # Add values on top of bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}',
                        ha='center', va='bottom')
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            img_buffer.seek(0)
            return Image(img_buffer, width=5*inch, height=3.5*inch)
        except Exception as e:
            logger.error(f"Failed to create bar chart: {e}")
            return None

class DatasetHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        datasets = Dataset.objects.filter(uploaded_by=request.user).order_by("-created_at")[:5]
        serializer = DatasetListSerializer(datasets, many=True)
        return Response(serializer.data)

    def delete(self, request):
        """Clear all dataset history for the authenticated user."""
        try:
            # Get all datasets for this user
            datasets = Dataset.objects.filter(uploaded_by=request.user)
            count = datasets.count()

            # Delete associated files and records
            for dataset in datasets:
                if dataset.file_path and os.path.exists(dataset.file_path):
                    try:
                        os.remove(dataset.file_path)
                    except OSError:
                        pass  # Log this in production
                dataset.delete()

            logger.info(f"User {request.user.username} cleared {count} datasets from history")
            return Response(
                {"message": f"Successfully cleared {count} datasets from history."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return Response(
                {"error": "Failed to clear history. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
             return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "message": "User created successfully", 
                "user_id": user.id,
                "token": token.key 
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "Login successful",
                    "user_id": user.id,
                    "username": user.username,
                    "token": token.key
                }
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class ValidateTokenView(APIView):
    """
    Validates if the provided authentication token is still valid.
    Used by frontend to verify stored tokens on app startup.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns user info if token is valid."""
        user = request.user
        return Response({
            "valid": True,
            "user_id": user.id,
            "username": user.username,
        })
