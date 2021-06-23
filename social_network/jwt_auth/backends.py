import jwt
from django.conf import settings
from .exceptions import TokenBackendError


class JWTBackend:

    @staticmethod
    def encode(payload):
        jwt_payload = payload.copy()
        token = jwt.encode(jwt_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return token

    @staticmethod
    def decode(token, verify=True):
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], verify=verify,
                options={"verify_signature": verify}
            )
        except jwt.InvalidTokenError:
            raise TokenBackendError('Token is invalid or expired')
