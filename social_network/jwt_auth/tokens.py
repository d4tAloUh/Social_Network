import datetime
import uuid
from calendar import timegm

from django.conf import settings
from .backends import JWTBackend
from .exceptions import TokenBackendError, TokenError
from django.utils.timezone import is_naive, make_aware, utc


class Token:
    token_type = None
    lifetime = None

    def __init__(self, token=None):
        self.token = token
        self.backend = JWTBackend
        # create token
        if token is None:
            self.payload = {'token_type': self.token_type}
            self.set_exp()
            self.set_jti()
        # verify token
        else:
            try:
                self.payload = self.backend.decode(token, verify=True)
            except TokenBackendError as e:
                raise TokenError(e)

            self.verify_token()

    def make_utc(self, date_time):
        if is_naive(date_time):
            return make_aware(date_time, timezone=utc)
        return date_time

    def set_exp(self):
        from_time = self.make_utc(datetime.datetime.utcnow())
        self.payload['exp'] = timegm((from_time + self.lifetime).utctimetuple())

    def __str__(self):
        return self.backend.encode(self.payload)

    def set_jti(self):
        self.payload['jti'] = uuid.uuid4().hex

    def verify_token(self):
        self.check_exp()
        self.check_jti()
        self.check_type()

    def check_jti(self):
        if 'jti' not in self.payload:
            raise TokenError("Token has no jti")

    def check_exp(self):
        try:
            exp_value = self.payload['exp']
        except KeyError:
            raise TokenError("Token has no expiration")

        utc_exc_value = self.make_utc(datetime.datetime.utcfromtimestamp(exp_value))

        if utc_exc_value < self.make_utc(datetime.datetime.utcnow()):
            raise TokenError("Token has expired")

    def check_type(self):
        try:
            token_type = self.payload['token_type']
        except KeyError:
            raise TokenError("Token has no type")

        if token_type != self.token_type:
            raise TokenError("Token has wrong type")

    @classmethod
    def for_user(cls, user):
        user_id = getattr(user, settings.USER_ID_FIELD)
        token = cls()
        token.payload[settings.USER_ID_FIELD] = user_id
        return token


class AccessToken(Token):
    token_type = 'access'
    lifetime = settings.ACCESS_TOKEN_LIFETIME


class RefreshToken(Token):
    token_type = 'refresh'
    lifetime = settings.REFRESH_TOKEN_LIFETIME
    unique_fields = ['token_type', 'exp', 'jti']

    def get_access_token(self):
        access = AccessToken()
        for claim, value in self.payload.items():
            if claim in self.unique_fields:
                continue
            access.payload[claim] = value
        return access
