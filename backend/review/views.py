from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ingestion.models import NormalizedRecord
from .serializers import NormalizedRecordListSerializer, ReviewUpdateSerializer
from django.utils import timezone
from audit.models import AuditLog

class ReviewList(APIView):
    """
    GET /api/review/ - list normalized records (supports ?q=)
    PUT /api/review/:id/ - update status (approved true/false)
    """
    def get(self, request):
        q = request.GET.get('q','').strip()
        qs = NormalizedRecord.objects.all().order_by('-id')
        if q:
            qs = qs.filter(activity_type__icontains=q) | qs.filter(scope__icontains=q)
        serializer = NormalizedRecordListSerializer(qs, many=True)
        return Response(serializer.data)

class ReviewUpdate(APIView):
    def put(self, request, id):
        serializer = ReviewUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        approved = serializer.validated_data['approved']
        try:
            rec = NormalizedRecord.objects.get(id=id)
        except NormalizedRecord.DoesNotExist:
            return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        rec.status = 'approved' if approved else 'rejected'
        rec.save()
        # log audit
        AuditLog.objects.create(user='system', action='approve' if approved else 'reject', record_id=rec.id)
        return Response({'detail':'updated'})
