"""
Charts View - Matplotlib visualizations for equipment data
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTabWidget, QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPainter

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from ..components.cards import AlertCard


class ChartToolbar(NavigationToolbar):
    """Customized matplotlib navigation toolbar"""
    
    def __init__(self, canvas, parent=None):
        super().__init__(canvas, parent)
        self.setIconSize(QSize(18, 18))
        self.setStyleSheet("""
            QToolBar {
                background-color: transparent;
                border: none;
                spacing: 4px; /* Tighter spacing */
                padding: 2px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 4px; /* Smaller padding */
                margin: 0px;
            }
            QToolButton:hover {
                background-color: #333333;
            }
            QToolButton:checked {
                background-color: #3D3D3D;
                border: 1px solid #555555;
            }
            QLabel {
                color: #888888;
                font-size: 11px;
                margin-left: 8px;
            }
        """)
        
        # Update icons immediately
        self._update_icons()
        
        # Activate pan by default
        self.pan()

    def _update_icons(self):
        """Recolor icons to match theme"""
        for action in self.actions():
            if action.icon() and not action.icon().isNull():
                icon = action.icon()
                # Use a larger source size to prevent degradation
                size = QSize(48, 48)
                pixmap = icon.pixmap(size)
                
                if not pixmap.isNull():
                    # Create new pixmap and recolor
                    colored_pixmap = QPixmap(pixmap.size())
                    colored_pixmap.fill(Qt.transparent)
                    
                    painter = QPainter(colored_pixmap)
                    painter.drawPixmap(0, 0, pixmap)
                    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                    painter.fillRect(colored_pixmap.rect(), QColor("#E8E8E8"))
                    painter.end()
                    
                    action.setIcon(QIcon(colored_pixmap))


class MplCanvas(FigureCanvas):
    """Matplotlib canvas for embedding charts"""
    
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        # Set style
        plt.style.use('dark_background')
        
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1A1A1A')
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#1A1A1A')
        
        # Style axes
        self.axes.spines['bottom'].set_color('#444444')
        self.axes.spines['top'].set_color('#444444')
        self.axes.spines['left'].set_color('#444444')
        self.axes.spines['right'].set_color('#444444')
        self.axes.tick_params(colors='#888888', labelsize=9)
        self.axes.xaxis.label.set_color('#E8E8E8')
        self.axes.yaxis.label.set_color('#E8E8E8')
        self.axes.title.set_color('#E8E8E8')
        
        super().__init__(fig)
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self, 
            QSizePolicy.Expanding, 
            QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class ChartsView(QWidget):
    """View for data visualization with charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.summary_data = {}
        self.equipment_data = []
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Data Visualization")
        header.setObjectName("heading")
        header.setFont(QFont("Source Sans 3", 24, QFont.Bold))
        layout.addWidget(header)
        
        # Tab widget for different charts
        self.tabs = QTabWidget()
        
        # Bar chart tab
        self.bar_tab = QWidget()
        bar_layout = QVBoxLayout(self.bar_tab)
        bar_layout.setContentsMargins(16, 16, 16, 16)
        
        self.bar_canvas = MplCanvas(self, width=10, height=6)
        self.bar_toolbar = ChartToolbar(self.bar_canvas, self.bar_tab)
        bar_layout.addWidget(self.bar_toolbar)
        bar_layout.addWidget(self.bar_canvas)
        
        self.tabs.addTab(self.bar_tab, "📊  Averages by Type")
        
        # Pie chart tab
        self.pie_tab = QWidget()
        pie_layout = QVBoxLayout(self.pie_tab)
        pie_layout.setContentsMargins(16, 16, 16, 16)
        
        self.pie_canvas = MplCanvas(self, width=8, height=6)
        self.pie_toolbar = ChartToolbar(self.pie_canvas, self.pie_tab)
        pie_layout.addWidget(self.pie_toolbar)
        pie_layout.addWidget(self.pie_canvas)
        
        self.tabs.addTab(self.pie_tab, "🥧  Type Distribution")
        
        # Scatter chart tab
        self.scatter_tab = QWidget()
        scatter_layout = QVBoxLayout(self.scatter_tab)
        scatter_layout.setContentsMargins(16, 16, 16, 16)
        
        self.scatter_canvas = MplCanvas(self, width=10, height=6)
        self.scatter_toolbar = ChartToolbar(self.scatter_canvas, self.scatter_tab)
        scatter_layout.addWidget(self.scatter_toolbar)
        scatter_layout.addWidget(self.scatter_canvas)
        
        self.tabs.addTab(self.scatter_tab, "📈  Temp vs Pressure")

        # Correlation tab
        self.corr_tab = QWidget()
        corr_layout = QVBoxLayout(self.corr_tab)
        corr_layout.setContentsMargins(16, 16, 16, 16)
        
        self.corr_canvas = MplCanvas(self, width=8, height=6)
        self.corr_toolbar = ChartToolbar(self.corr_canvas, self.corr_tab)
        corr_layout.addWidget(self.corr_toolbar)
        corr_layout.addWidget(self.corr_canvas)
        
        self.tabs.addTab(self.corr_tab, "🔥  Correlation")
        
        # Histogram tab
        self.hist_tab = QWidget()
        hist_layout = QVBoxLayout(self.hist_tab)
        hist_layout.setContentsMargins(16, 16, 16, 16)
        
        self.hist_canvas = MplCanvas(self, width=10, height=6)
        self.hist_toolbar = ChartToolbar(self.hist_canvas, self.hist_tab)
        hist_layout.addWidget(self.hist_toolbar)
        hist_layout.addWidget(self.hist_canvas)
        
        self.tabs.addTab(self.hist_tab, "📊  Distributions")
        
        layout.addWidget(self.tabs)
        
        # No data placeholder
        self.no_data_alert = AlertCard(
            "No data available for visualization. Upload a dataset first.",
            "info"
        )
        layout.addWidget(self.no_data_alert)
        self.no_data_alert.hide()
    
    def set_data(self, summary: dict, equipment: list):
        """Update charts with new data"""
        self.summary_data = summary
        self.equipment_data = equipment
        
        if not equipment:
            self.tabs.hide()
            self.no_data_alert.show()
            return
        
        self.tabs.show()
        self.no_data_alert.hide()
        
        self._draw_bar_chart()
        self._draw_pie_chart()
        self._draw_bar_chart()
        self._draw_pie_chart()
        self._draw_scatter_chart()
        self._draw_correlation_chart()
        self._draw_histogram_chart()
    
    def _draw_bar_chart(self):
        """Draw bar chart showing averages by equipment type"""
        ax = self.bar_canvas.axes
        ax.clear()
        
        if not self.equipment_data:
            return
        
        # Calculate averages by type
        type_data = {}
        for eq in self.equipment_data:
            eq_type = eq.get('equipment_type', 'Unknown')
            if eq_type not in type_data:
                type_data[eq_type] = {'flow': [], 'pressure': [], 'temp': []}
            type_data[eq_type]['flow'].append(eq.get('flowrate', 0))
            type_data[eq_type]['pressure'].append(eq.get('pressure', 0))
            type_data[eq_type]['temp'].append(eq.get('temperature', 0))
        
        types = list(type_data.keys())
        avg_flow = [sum(type_data[t]['flow'])/len(type_data[t]['flow']) for t in types]
        avg_pres = [sum(type_data[t]['pressure'])/len(type_data[t]['pressure']) for t in types]
        avg_temp = [sum(type_data[t]['temp'])/len(type_data[t]['temp']) for t in types]
        
        x = range(len(types))
        width = 0.25
        
        # Colors
        colors = ['#00D9A5', '#FF6B35', '#00A8E8']
        
        bars1 = ax.bar([i - width for i in x], avg_flow, width, label='Flowrate', color=colors[0])
        bars2 = ax.bar(x, avg_pres, width, label='Pressure', color=colors[1])
        bars3 = ax.bar([i + width for i in x], avg_temp, width, label='Temperature', color=colors[2])
        
        ax.set_xlabel('Equipment Type', fontsize=10, color='#E8E8E8')
        ax.set_ylabel('Average Value', fontsize=10, color='#E8E8E8')
        ax.set_title('Average Parameters by Equipment Type', fontsize=12, fontweight='bold', color='#FFFFFF', pad=16)
        ax.set_xticks(x)
        ax.set_xticklabels(types, rotation=45, ha='right', fontsize=9)
        ax.legend(loc='upper right', facecolor='#252525', edgecolor='#444444', fontsize=9)
        ax.grid(axis='y', alpha=0.3, color='#444444')
        
        try:
            self.bar_canvas.figure.tight_layout()
        except Exception:
            pass  # Ignore layout errors on small canvas
        self.bar_canvas.draw()
    
    def _draw_pie_chart(self):
        """Draw pie chart showing type distribution"""
        ax = self.pie_canvas.axes
        ax.clear()
        
        distribution = self.summary_data.get('type_distribution', {})
        if not distribution:
            return
        
        labels = list(distribution.keys())
        sizes = list(distribution.values())
        
        # Custom colors
        colors = ['#00D9A5', '#FF6B35', '#00A8E8', '#FFD166', '#EF476F', '#8338EC']
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors[:len(labels)],
            startangle=90,
            explode=[0.02] * len(labels),
            textprops={'color': '#E8E8E8', 'fontsize': 10}
        )
        
        for autotext in autotexts:
            autotext.set_color('#0D0D0D')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title('Equipment Type Distribution', fontsize=12, fontweight='bold', color='#FFFFFF', pad=16)
        
        try:
            self.pie_canvas.figure.tight_layout()
        except Exception:
            pass  # Ignore layout errors on small canvas
        self.pie_canvas.draw()
    
    def _draw_scatter_chart(self):
        """Draw scatter plot of temperature vs pressure"""
        ax = self.scatter_canvas.axes
        ax.clear()
        
        if not self.equipment_data:
            return
        
        temps = [eq.get('temperature', 0) for eq in self.equipment_data]
        pressures = [eq.get('pressure', 0) for eq in self.equipment_data]
        types = [eq.get('equipment_type', 'Unknown') for eq in self.equipment_data]
        
        # Color by type
        unique_types = list(set(types))
        colors = ['#00D9A5', '#FF6B35', '#00A8E8', '#FFD166', '#EF476F', '#8338EC']
        type_colors = {t: colors[i % len(colors)] for i, t in enumerate(unique_types)}
        
        for eq_type in unique_types:
            type_temps = [temps[i] for i in range(len(temps)) if types[i] == eq_type]
            type_pres = [pressures[i] for i in range(len(pressures)) if types[i] == eq_type]
            ax.scatter(type_temps, type_pres, c=type_colors[eq_type], label=eq_type, alpha=0.7, s=60)
        
        ax.set_xlabel('Temperature', fontsize=10, color='#E8E8E8')
        ax.set_ylabel('Pressure', fontsize=10, color='#E8E8E8')
        ax.set_title('Temperature vs Pressure Correlation', fontsize=12, fontweight='bold', color='#FFFFFF', pad=16)
        ax.legend(loc='upper right', facecolor='#252525', edgecolor='#444444', fontsize=9)
        ax.grid(alpha=0.3, color='#444444')
        
        try:
            self.scatter_canvas.figure.tight_layout()
        except Exception:
            pass  # Ignore layout errors on small canvas
        self.scatter_canvas.draw()

    def _draw_correlation_chart(self):
        """Draw correlation heatmap"""
        ax = self.corr_canvas.axes
        ax.clear()
        
        if not self.equipment_data:
            return
            
        # Extract data
        temps = [eq.get('temperature', 0) for eq in self.equipment_data]
        pressures = [eq.get('pressure', 0) for eq in self.equipment_data]
        flows = [eq.get('flowrate', 0) for eq in self.equipment_data]
        
        # Compute correlation matrix
        data = np.array([flows, pressures, temps])
        corr_matrix = np.corrcoef(data)
        labels = ['Flow', 'Pressure', 'Temp']
        
        # Plot heatmap
        im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        
        # Add colorbar
        if not hasattr(self, 'corr_cbar'):
            self.corr_cbar = self.corr_canvas.figure.colorbar(im, ax=ax)
            self.corr_cbar.ax.yaxis.set_tick_params(color='#888888', labelcolor='#888888', labelsize=9)
            self.corr_cbar.outline.set_edgecolor('#444444')
        else:
            self.corr_cbar.update_normal(im)
            
        # Show values
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = ax.text(j, i, f"{corr_matrix[i, j]:.2f}",
                             ha="center", va="center", color="white",
                             fontweight="bold", fontsize=10)
                             
        ax.set_xticks(np.arange(len(labels)))
        ax.set_yticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_yticklabels(labels, fontsize=10)
        
        ax.set_title('Parameter Correlation Matrix', fontsize=12, fontweight='bold', color='#FFFFFF', pad=16)
        self.corr_canvas.draw()
        
    def _draw_histogram_chart(self):
        """Draw distributions for parameters"""
        fig = self.hist_canvas.figure
        fig.clear()
        
        if not self.equipment_data:
            return
            
        # Extract data
        flows = [eq.get('flowrate', 0) for eq in self.equipment_data]
        pressures = [eq.get('pressure', 0) for eq in self.equipment_data]
        temps = [eq.get('temperature', 0) for eq in self.equipment_data]
        
        # Create subplots (1 row, 3 columns)
        axes = fig.subplots(1, 3)
        
        params = [
            (flows, 'Flowrate', '#00D9A5'),
            (pressures, 'Pressure', '#FF6B35'),
            (temps, 'Temperature', '#00A8E8')
        ]
        
        for i, (data, label, color) in enumerate(params):
            ax = axes[i]
            ax.set_facecolor('#1A1A1A')
            ax.spines['bottom'].set_color('#444444')
            ax.spines['top'].set_color('#444444')
            ax.spines['left'].set_color('#444444')
            ax.spines['right'].set_color('#444444')
            ax.tick_params(colors='#888888', labelsize=9)
            
            ax.hist(data, bins=15, color=color, alpha=0.7, rwidth=0.9)
            ax.set_title(f'{label} Dist.', color='#E8E8E8', fontsize=11, fontweight='bold')
            ax.grid(axis='y', alpha=0.3, color='#444444')
            
        fig.suptitle('Parameter Distributions', color='white', fontsize=12, fontweight='bold', y=0.95)
        
        try:
            fig.tight_layout()
        except Exception:
            pass
        self.hist_canvas.draw()
