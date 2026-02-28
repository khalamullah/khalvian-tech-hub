from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.api_devices, name='api_devices'),
    path('notifications/', views.api_notifications, name='api_notifications'),
    path('devices/<str:device_id>/status/', views.api_device_status, name='api_device_status'),
]