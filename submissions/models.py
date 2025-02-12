from django.db import models
from programs.models import Program
import uuid

# Create your models here.
class Submission(models.Model):
    SERVERITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('triaged', 'Triaged'),
        ('review', 'Review'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected')
    ]
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=6, choices=SERVERITY_CHOICES)
    evidence = models.FileField(upload_to='evidence_attachments/', blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='triaged')

    def __str__(self):
        return self.title