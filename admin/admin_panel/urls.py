"""
URL configuration for admin_panel project.
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", admin.site.urls),
]
