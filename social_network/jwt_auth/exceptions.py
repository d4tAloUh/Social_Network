from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed


class TokenError(Exception):
    pass


class TokenBackendError(Exception):
    pass

