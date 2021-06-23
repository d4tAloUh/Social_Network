from django.urls import path

from .views.user import UserRetrieveAPIView

urlpatterns = [
    path(r'users/', UserRetrieveAPIView.as_view(), name='user-list')
]
