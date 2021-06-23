from rest_framework import generics, mixins
from ..serializers import UserModelSerializer, UserRegistrationSerializer
from ..models import CustomUser
from rest_framework.permissions import IsAuthenticated


class UserRetrieveView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserModelSerializer
    queryset = CustomUser.objects.all()


class UserRetrieveListAPIView(UserRetrieveView, generics.ListAPIView):
    pass


class UserRetrieveAPIView(UserRetrieveView, generics.RetrieveAPIView):
    pass


class UserRegistrationApiView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
