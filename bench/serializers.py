from rest_framework import serializers
from .models import Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = [
            "id",
            "name",
            "description",
            "value",
            "lce",
            "prt",
            "smo",
            "dept",
            "clbc",
            "created_at",
            "updated_at",
        ]
