from django.db import models
from ingestion.models import NormalizedRecord

class ReviewRecord(models.Model):
    record = models.OneToOneField(NormalizedRecord, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)