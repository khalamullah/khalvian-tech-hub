from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_view, name='blog'),
    path('create/', views.post_create_view, name='post_create'),
    path('<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
]