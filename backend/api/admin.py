from django.contrib import admin
from .models import Dataset, Equipment, DatasetSummary


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "uploaded_by", "created_at", "row_count"]
    search_fields = ["name"]
    list_filter = ["created_at"]


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "equipment_name",
        "equipment_type",
        "flowrate",
        "pressure",
        "temperature",
    ]
    search_fields = ["equipment_name", "equipment_type"]
    list_filter = ["equipment_type"]


@admin.register(DatasetSummary)
class DatasetSummaryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "dataset",
        "total_count",
        "avg_flowrate",
        "avg_pressure",
        "avg_temperature",
    ]
    search_fields = ["dataset__name"]
