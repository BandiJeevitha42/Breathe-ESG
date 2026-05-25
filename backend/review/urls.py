from django.urls import path
from .views import ReviewList, ReviewUpdate

urlpatterns = [
    path('review/', ReviewList.as_view(), name='api-review-list'),
    path('review/<int:id>/', ReviewUpdate.as_view(), name='api-review-update'),
]