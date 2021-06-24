from django.urls import path

from .views import ReactionAnalyticsAPIView

urlpatterns = [
    path(r'analytics/', ReactionAnalyticsAPIView.as_view(), name='analytics')
]

