from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class TokenView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# Create your views here.
class TokenObtainAPIView(TokenView):
    serializer_class = TokenObtainPairSerializer


class TokenRefreshAPIView(TokenView):
    serializer_class = TokenRefreshSerializer
