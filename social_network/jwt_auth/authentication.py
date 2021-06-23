from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from rest_framework.authentication import get_authorization_header
from .tokens import AccessToken
from .exceptions import TokenError


class JWTAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = 'api'
    keyword = 'Bearer'

    def __init__(self):
        self.user_model = get_user_model()

    def authenticate(self, request):
        header_parts = get_authorization_header(request).split()

        if not header_parts or header_parts[0].lower() != self.keyword.lower().encode():
            return None

        if len(header_parts) == 1:
            msg = 'No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(header_parts) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            raw_token = header_parts[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_validated_token(self, raw_token):
        try:
            return AccessToken(token=raw_token)
        except TokenError as exc:
            raise exceptions.AuthenticationFailed(exc)

    def get_user(self, validated_token):
        try:
            user_id = validated_token.payload['user_id']
        except KeyError:
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user = self.user_model.objects.get(id=user_id)
        except self.user_model.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found', code='user_not_found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive', code='user_inactive')

        return user

    def authenticate_header(self, request):
        return self.keyword
