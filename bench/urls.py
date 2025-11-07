from django.urls import path
from . import views

urlpatterns = [
    path("metrics/data/", views.metrics_list, name="metrics-data"),
    path("health/", views.health_check, name="health"),
]
