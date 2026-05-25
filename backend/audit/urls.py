from django.urls import path
from .views import AuditList

urlpatterns = [
    path('audit/', AuditList.as_view(), name='api-audit-list'),
]