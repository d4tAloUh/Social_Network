from django.urls import path

from .views import UserRetrieveAPIView, UserRegistrationApiView, PostCreationAPIView, ReactionListAPIView

urlpatterns = [
    path(r'users/', UserRetrieveAPIView.as_view(), name='user-list'),
    path(r'users/registration/', UserRegistrationApiView.as_view(), name='user-registration'),
    path(r'posts/', PostCreationAPIView.as_view(), name='post-creation'),
    path(r'reactions/', ReactionListAPIView.as_view(), name='reactions')
]
