from django.urls import path
from . import views

urlpatterns = [
    # These are included under "/api/" from config.urls
    path("metrics/ingest", views.api_ingest, name="api-metrics-ingest"),
    path("metrics/data/", views.api_metrics_data, name="api-metrics-data"),
]
