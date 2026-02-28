from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list_view, name='file_list'),
    path('upload/', views.file_upload_view, name='file_upload'),
    path('<int:pk>/delete/', views.file_delete_view, name='file_delete'),
    path('<int:pk>/download/', views.file_download_view, name='file_download'),
]