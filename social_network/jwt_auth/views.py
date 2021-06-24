from rest_framework import generics, status
from rest_framework.response import Response

from .exceptions import TokenError
from .serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class TokenView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# Create your views here.
class TokenObtainAPIView(TokenView):
    serializer_class = TokenObtainPairSerializer


class TokenRefreshAPIView(TokenView):
    serializer_class = TokenRefreshSerializer
