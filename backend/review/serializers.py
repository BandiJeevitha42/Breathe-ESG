from rest_framework import serializers
from ingestion.models import NormalizedRecord
from .models import ReviewRecord

class NormalizedRecordListSerializer(serializers.ModelSerializer):
    source_type = serializers.SerializerMethodField()
    class Meta:
        model = NormalizedRecord
        fields = ['id', 'scope', 'activity_type', 'quantity', 'unit', 'status', 'source_type']

    def get_source_type(self, obj):
        return obj.raw_record.source.source_type

class ReviewUpdateSerializer(serializers.Serializer):
    approved = serializers.BooleanField()