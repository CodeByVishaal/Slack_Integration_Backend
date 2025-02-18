from django.db import models
from usermanagement.models import User
import uuid

# Create your models here.

class Program(models.Model):
    SERVERITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
    ]
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='programs', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=6, choices=SERVERITY_CHOICES)
    taxonomy = models.FileField(upload_to='taxonomy_documents/', blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title