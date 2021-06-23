from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from api.models import CustomUser
from .tokens import RefreshToken
from django.contrib.auth.models import update_last_login


class TokenObtainSerializer(serializers.Serializer):
    user = None
    password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField()

    def validate(self, attrs):
        self.user = authenticate(email=attrs['email'], password=attrs['password'])
        if self.user is None:
            raise serializers.ValidationError('Provided credentials are not valid')
        if not self.user.is_active:
            raise serializers.ValidationError('User is not active')
        return {}


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.get_access_token())

        update_last_login(None, self.user)

        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.ReadOnlyField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.get_access_token())}
        return data
