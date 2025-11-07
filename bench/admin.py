from django.contrib import admin
from .models import Metric


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "lce", "prt", "smo", "dept", "clbc", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
