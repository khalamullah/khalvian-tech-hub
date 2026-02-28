from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list_view, name='notifications'),
    path('<int:pk>/delete/', views.notification_delete_view, name='notification_delete'),
]