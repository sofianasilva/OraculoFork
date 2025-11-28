"""
URL configuration for Oráculo Authentication Service.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_service.users.urls')),
]