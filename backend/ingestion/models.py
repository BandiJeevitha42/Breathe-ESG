from django.db import models
from companies.models import Company

class DataSource(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    source_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_type} @ {self.uploaded_at}"

class RawRecord(models.Model):
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    raw_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class NormalizedRecord(models.Model):
    raw_record = models.OneToOneField(RawRecord, on_delete=models.CASCADE)
    scope = models.CharField(max_length=100, blank=True)
    activity_type = models.CharField(max_length=100, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, default='pending')  # pending/approved/rejected