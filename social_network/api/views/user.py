from rest_framework import generics
from ..serializers import UserModelSerializer, UserSerializer
from ..models import CustomUser
from rest_framework.permissions import IsAuthenticated


class UserRetrieveAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer
    queryset = CustomUser.objects.all()


class UserRegistrationApiView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
