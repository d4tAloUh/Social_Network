from django.test import TestCase
from rest_framework import exceptions
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from .authentication import JWTAuthentication

# Create your tests here.
from api.models import CustomUser


class JWTAuthTest(APITestCase):

    def setUp(self) -> None:
        self.invalid_token = 'bla.bla.bla'
        self.user = CustomUser.objects.create(**{
            "email": "test@gmail.com",
            "password": "qwe123"
        })
        self.invalid_header = 'Bearer ' + self.invalid_token
        self.invalid_keyword_header = 'Token ' + self.invalid_token
        self.invalid_parts_header = 'Bearer ' + self.invalid_token + ' Token'
        self.jwt_auth = JWTAuthentication()
        self.factory = APIRequestFactory()

    def test_wrong_token_header(self):
        request = self.factory.get('/bla/')

        # without http auth header returns no user
        self.assertIsNone(self.jwt_auth.authenticate(request))

    def test_wrong_keyword_header(self):
        request = self.factory.get('/bla/', HTTP_AUTHORIZATION=self.invalid_keyword_header)
        self.assertIsNone(self.jwt_auth.authenticate(request))

    def test_wrong_parts_header(self):
        # contains 3 pairs instead of 2
        request = self.factory.get('/bla/', HTTP_AUTHORIZATION=self.invalid_parts_header)
        with self.assertRaises(exceptions.AuthenticationFailed):
            self.jwt_auth.authenticate(request)

    def test_invalid_token(self):
        # jwt validation error
        request = self.factory.get('/bla/', HTTP_AUTHORIZATION=self.invalid_header)
        with self.assertRaises(exceptions.AuthenticationFailed):
            self.jwt_auth.authenticate(request)

class JWTViewsTest(APITestCase):
