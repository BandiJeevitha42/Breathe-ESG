from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class AuditList(APIView):
    def get(self, request):
        qs = AuditLog.objects.all().order_by('-timestamp')
        paginator = PageNumberPagination()
        paginator.page_size = 25
        page = paginator.paginate_queryset(qs, request)
        serializer = AuditLogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
