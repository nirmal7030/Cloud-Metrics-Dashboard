from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Metric
from .serializers import MetricSerializer


def dashboard_view(request):
    """
    Render the web dashboard that consumes the metrics API.
    """
    return render(request, "bench/dashboard.html")


@api_view(["GET"])
def metrics_list(request):
    """
    Return all metrics as JSON.
    """
    metrics = Metric.objects.all()
    serializer = MetricSerializer(metrics, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def health_check(request):
    """
    Simple health endpoint used for Docker/EC2 checks.
    """
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
