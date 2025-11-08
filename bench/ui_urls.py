from django.urls import path
from . import views

urlpatterns = [
    # Dashboard HTML at the root "/"
    path("", views.dashboard, name="dashboard"),
]
