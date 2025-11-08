from django.urls import path
from . import views

urlpatterns = [
    path("metrics/data/", views.metrics_list, name="metrics-data"),
    path("health/", views.health_check, name="health"),
]
from django.urls import path
from .views import api_ingest, api_metrics_data

urlpatterns = [
    path("api/metrics/data/", api_metrics_data, name="api-metrics-data"),
    path("api/metrics/ingest", api_ingest, name="api-metrics-ingest"),  # no trailing slash to match curl
]
