from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list_view, name='device_list'),
    path('add/', views.device_create_view, name='device_create'),
    path('<int:pk>/', views.device_detail_view, name='device_detail'),
    path('<int:pk>/edit/', views.device_edit_view, name='device_edit'),
    path('<int:pk>/delete/', views.device_delete_view, name='device_delete'),
]