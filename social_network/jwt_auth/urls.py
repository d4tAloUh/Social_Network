from django.urls import path
from .views import TokenObtainAPIView, TokenRefreshAPIView

urlpatterns = [
    path(r'token/', TokenObtainAPIView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh', TokenRefreshAPIView.as_view(), name='token_refresh')
]
