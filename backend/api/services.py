import pandas as pd
from django.db import transaction
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Dataset, Equipment, DatasetSummary
import os

REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']

class DatasetService:
    @staticmethod
    def validate_csv(df):
        """
        Validates that the CSV contains necessary columns.
        """
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Validate data types
        try:
            pd.to_numeric(df['Flowrate'])
            pd.to_numeric(df['Pressure'])
            pd.to_numeric(df['Temperature'])
        except ValueError:
            raise ValueError("Flowrate, Pressure, and Temperature must be numeric values.")

    @staticmethod
    def process_dataset(file, user):
        """
        Handles the full process of saving file, parsing CSV, saving to DB, and generating summary.
        """
        # Save file temporarily or permanently depending on storage backend
        file_path = default_storage.save(f"uploads/{file.name}", file)
        full_path = default_storage.path(file_path)

        try:
            df = pd.read_csv(full_path)
            # Normalize headers
            df.columns = [c.strip() for c in df.columns]
            
            DatasetService.validate_csv(df)

            with transaction.atomic():
                # Create Dataset Record
                dataset = Dataset.objects.create(
                    name=file.name,
                    uploaded_by=user,
                    row_count=len(df),
                    file_path=full_path
                )

                # Bulk Create Equipment
                equipment_list = [
                    Equipment(
                        dataset=dataset,
                        equipment_name=str(row['Equipment Name']).strip(),
                        equipment_type=str(row['Type']).strip(),
                        flowrate=float(row['Flowrate']),
                        pressure=float(row['Pressure']),
                        temperature=float(row['Temperature'])
                    )
                    for _, row in df.iterrows()
                ]
                Equipment.objects.bulk_create(equipment_list)

                # Generate and Save Summary
                summary_data = DatasetService.generate_summary(df)
                DatasetSummary.objects.create(dataset=dataset, **summary_data)
                
                # Cleanup Old Datasets (Keep max 5)
                DatasetService.cleanup_old_datasets()

                return dataset

        except Exception as e:
            # If anything fails, ensure we don't leave a file hanging if we can help it, 
            # though transaction rollback handles DB.
            if os.path.exists(full_path):
                os.remove(full_path)
            raise e

    @staticmethod
    def generate_summary(df):
        return {
            "total_count": len(df),
            "avg_flowrate": df["Flowrate"].mean(),
            "avg_pressure": df["Pressure"].mean(),
            "avg_temperature": df["Temperature"].mean(),
            "type_distribution": df["Type"].value_counts().to_dict(),
            "min_flowrate": df["Flowrate"].min(),
            "max_flowrate": df["Flowrate"].max(),
            "min_pressure": df["Pressure"].min(),
            "max_pressure": df["Pressure"].max(),
            "min_temperature": df["Temperature"].min(),
            "max_temperature": df["Temperature"].max(),
        }

    @staticmethod
    def cleanup_old_datasets():
        """
        Maintains only the last 5 datasets. Deletes older ones including files.
        """
        # Get IDs of the last 5 datasets
        last_5_ids = Dataset.objects.order_by('-created_at').values_list('id', flat=True)[:5]
        
        # Find datasets NOT in the last 5
        datasets_to_delete = Dataset.objects.exclude(id__in=last_5_ids)
        
        for dataset in datasets_to_delete:
            if dataset.file_path and os.path.exists(dataset.file_path):
                try:
                    os.remove(dataset.file_path)
                except OSError:
                    pass # Log this in production
            dataset.delete()
