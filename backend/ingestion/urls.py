from django.urls import path
from .views import UploadView, DashboardView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='api-upload'),
    path('dashboard/', DashboardView.as_view(), name='api-dashboard'),
]