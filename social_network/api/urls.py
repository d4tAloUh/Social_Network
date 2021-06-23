from django.urls import path

from .views.user import UserRetrieveAPIView, UserRegistrationApiView

urlpatterns = [
    path(r'users/', UserRetrieveAPIView.as_view(), name='user-list'),
    path(r'users/registration/', UserRegistrationApiView.as_view(), name='user-registration')
]
