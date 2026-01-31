from rest_framework import serializers
from .models import Dataset, Equipment, DatasetSummary


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            "id",
            "equipment_name",
            "equipment_type",
            "flowrate",
            "pressure",
            "temperature",
        ]


class DatasetSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetSummary
        fields = [
            "total_count",
            "avg_flowrate",
            "avg_pressure",
            "avg_temperature",
            "type_distribution",
            "min_flowrate",
            "max_flowrate",
            "min_pressure",
            "max_pressure",
            "min_temperature",
            "max_temperature",
        ]


class DatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    summary = DatasetSummarySerializer(read_only=True)

    class Meta:
        model = Dataset
        fields = ["id", "name", "created_at", "row_count", "equipment", "summary"]


class DatasetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "name", "created_at", "row_count"]
