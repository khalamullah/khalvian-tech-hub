from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_id', 'user', 'status', 'ip_address', 'last_seen']
    list_filter = ['status']
    search_fields = ['name', 'device_id', 'user__username']
    ordering = ['-created_at']