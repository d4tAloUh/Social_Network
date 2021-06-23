from django.urls import path

from .views import UserRetrieveAPIView, UserRegistrationApiView, PostCreationAPIView, ReactionListAPIView, \
    UserRetrieveListAPIView

urlpatterns = [
    path(r'users/', UserRetrieveListAPIView.as_view(), name='user-list'),
    path(r'users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-list'),
    path(r'users/registration/', UserRegistrationApiView.as_view(), name='user-registration'),

    path(r'posts/', PostCreationAPIView.as_view(), name='post-creation'),
    path(r'reactions/', ReactionListAPIView.as_view(), name='reactions'),

    path(r'analytics/', ReactionListAPIView.as_view(), name='analytics')
]
