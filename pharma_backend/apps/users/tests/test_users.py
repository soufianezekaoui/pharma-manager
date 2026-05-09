"""
Tests for the Users / Auth module.
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import User


class AuthAPITest(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.pharmacist = User.objects.create_user(
            username="pharmacist1",
            email="ph@pharma.ma",
            password="Test1234!",
            role="pharmacist",
        )

    def _get_tokens(self, username="pharmacist1", password="Test1234!"):
        resp = self.client_api.post(
            "/api/auth/login/",
            {"username": username, "password": password},
            format="json",
        )
        return resp.data

    def test_register(self):
        resp = self.client_api.post(
            "/api/auth/register/",
            {
                "username": "newclient",
                "email": "nc@pharma.ma",
                "password": "Test1234!",
                "password2": "Test1234!",
                "role": "client",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", resp.data)

    def test_register_password_mismatch(self):
        resp = self.client_api.post(
            "/api/auth/register/",
            {
                "username": "newclient2",
                "email": "nc2@pharma.ma",
                "password": "Test1234!",
                "password2": "Wrong123!",
                "role": "client",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        tokens = self._get_tokens()
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)

    def test_login_wrong_password(self):
        resp = self.client_api.post(
            "/api/auth/login/",
            {"username": "pharmacist1", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_endpoint(self):
        tokens = self._get_tokens()
        self.client_api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        resp = self.client_api.get("/api/auth/me/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["data"]["username"], "pharmacist1")

    def test_logout(self):
        tokens = self._get_tokens()
        self.client_api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        resp = self.client_api.post(
            "/api/auth/logout/",
            {"refresh": tokens["refresh"]},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
