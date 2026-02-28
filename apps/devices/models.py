from django.db import models
from django.core.validators import RegexValidator
from apps.accounts.models import User


class Device(models.Model):
    STATUS_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('idle', 'Idle'),
    )

    device_id_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]+$',
        message='Device ID can only contain letters, numbers, hyphens and underscores.'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='devices',
        db_index=True
    )
    name = models.CharField(max_length=100)
    device_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        validators=[device_id_validator]
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='offline',
        db_index=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.device_id})'

    def is_online(self):
        return self.status == 'online'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['status']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['-last_seen']),
        ]