from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'size', 'mimetype', 'uploaded_at']
    list_filter = ['mimetype']
    search_fields = ['name', 'user__username']
    ordering = ['-uploaded_at']