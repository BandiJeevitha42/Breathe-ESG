import csv
import io
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DataSource, RawRecord, NormalizedRecord
from .serializers import RawRecordSerializer, NormalizedRecordSerializer

class UploadView(APIView):
    """
    POST /api/upload/ - accepts multipart file and source_type
    Parses CSV or JSON into RawRecord and creates basic NormalizedRecord placeholders.
    """
    def post(self, request):
        f = request.FILES.get('file')
        source_type = request.POST.get('source_type', 'generic')
        if not f:
            return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # create DataSource
        ds = DataSource.objects.create(source_type=source_type)

        # attempt to parse CSV, otherwise JSON
        text = f.read().decode('utf-8')
        created = 0
        try:
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                raw = RawRecord.objects.create(source=ds, raw_data=row)
                NormalizedRecord.objects.create(raw_record=raw, scope=row.get('scope', ''), activity_type=row.get('activity_type', ''), quantity=_safe_float(row.get('quantity')), unit=row.get('unit',''))
                created += 1
        except Exception:
            # try JSON array
            try:
                arr = json.loads(text)
                if isinstance(arr, dict):
                    arr = [arr]
                for obj in arr:
                    raw = RawRecord.objects.create(source=ds, raw_data=obj)
                    NormalizedRecord.objects.create(raw_record=raw, scope=obj.get('scope', ''), activity_type=obj.get('activity_type', ''), quantity=_safe_float(obj.get('quantity')), unit=obj.get('unit',''))
                    created += 1
            except Exception:
                return Response({'detail': 'Failed to parse file'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': f'Uploaded {created} records'}, status=status.HTTP_201_CREATED)

def _safe_float(v):
    try:
        return float(v)
    except Exception:
        return None

class DashboardView(APIView):
    """
    GET /api/dashboard/ - returns aggregated stats
    """
    def get(self, request):
        total = NormalizedRecord.objects.count()
        pending = NormalizedRecord.objects.filter(status='pending').count()
        approved = NormalizedRecord.objects.filter(status='approved').count()
        failed = NormalizedRecord.objects.filter(status='failed').count()
        # simple monthly trend: group by month on RawRecord.created_at
        from django.db.models import Count
        from django.db.models.functions import TruncMonth
        months = RawRecord.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        monthly_trend = [{ 'month': m['month'].strftime('%Y-%m'), 'count': m['count'] } for m in months]
        # scope distribution
        scopes = NormalizedRecord.objects.values('scope').annotate(count=Count('id')).order_by('-count')
        scope_distribution = [{ 'scope': s['scope'] or 'unspecified', 'count': s['count'] } for s in scopes]
        return Response({
            'total_records': total,
            'pending_reviews': pending,
            'approved_records': approved,
            'failed_records': failed,
            'monthly_trend': monthly_trend,
            'scope_distribution': scope_distribution
        })