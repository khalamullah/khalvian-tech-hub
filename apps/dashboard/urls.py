from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/users/', views.admin_users_view, name='admin_users'),
    path('admin/devices/', views.admin_devices_view, name='admin_devices'),
    path('admin/messages/', views.admin_messages_view, name='admin_messages'),
]