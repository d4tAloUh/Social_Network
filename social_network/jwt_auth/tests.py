
from rest_framework import exceptions
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from .authentication import JWTAuthentication

# Create your tests here.
from api.models import CustomUser

from .tokens import RefreshToken

class JWTAuthTest(APITestCase):

    def setUp(self) -> None:
        self.invalid_token = 'bla.bla.bla'
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
    def setUp(self):
        CustomUser.objects.create_user(email="test31@gmail.com",
                                       password="qwe123")

    def test_invalid_login_data(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)

        response = self.client.post(url, {"email": "test@gmail.com"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)

        response = self.client.post(url, {"password": "qwe123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {"password": "qwe123",
                                          "email": "test1@gmail.com"})

        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)

    def test_successful_login(self):
        url = reverse('token_obtain_pair')

        response = self.client.post(url, {
            "email": "test31@gmail.com",
            "password": "qwe123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_refresh_token_successfully(self):
        token = RefreshToken()
        url = reverse('token_refresh')

        response = self.client.post(url, {
           "refresh": str(token)
        })

        self.assertEqual(response.status_code, 200)

    def test_invalid_refresh_token(self):
        token = RefreshToken()
        del token.payload['token_type']

        url = reverse('token_refresh')
        response = self.client.post(url, {
            "refresh": str(token)
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)
