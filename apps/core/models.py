from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.name} - {self.subject}'

    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['is_read']),
            models.Index(fields=['-submitted_at']),
            models.Index(fields=['email']),
        ]