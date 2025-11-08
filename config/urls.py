from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard at "/"
    path("", include("bench.ui_urls")),

    # APIs under "/api/"
    path("api/", include("bench.urls")),
]
