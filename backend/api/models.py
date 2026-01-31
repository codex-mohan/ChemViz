from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(default=0)
    file_path = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name="equipment"
    )
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()

    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"


class DatasetSummary(models.Model):
    dataset = models.OneToOneField(
        Dataset, on_delete=models.CASCADE, related_name="summary"
    )
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField()
    min_flowrate = models.FloatField()
    max_flowrate = models.FloatField()
    min_pressure = models.FloatField()
    max_pressure = models.FloatField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()

    def __str__(self):
        return f"Summary for {self.dataset.name}"
