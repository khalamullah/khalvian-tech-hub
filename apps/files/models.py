from django.db import models
from django.core.validators import FileExtensionValidator
from apps.accounts.models import User
import os


ALLOWED_EXTENSIONS = [
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'txt', 'csv', 'json', 'xml',
    'jpg', 'jpeg', 'png', 'gif', 'webp',
    'zip', 'rar', 'tar', 'gz',
    'mp4', 'mp3', 'wav'
]


class UploadedFile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files',
        db_index=True
    )
    name = models.CharField(max_length=200, db_index=True)
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    size = models.PositiveBigIntegerField(default=0)
    mimetype = models.CharField(max_length=100, blank=True, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.basename(self.file.name)
        if self.file:
            self.size = self.file.size
        super().save(*args, **kwargs)

    def get_size_display(self):
        if self.size < 1024:
            return f'{self.size} B'
        elif self.size < 1024 * 1024:
            return f'{self.size / 1024:.1f} KB'
        else:
            return f'{self.size / (1024 * 1024):.1f} MB'

    def get_extension(self):
        return os.path.splitext(self.name)[1].lower()

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', '-uploaded_at']),
            models.Index(fields=['mimetype']),
            models.Index(fields=['-uploaded_at']),
        ]