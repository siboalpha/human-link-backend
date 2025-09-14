from core.tests.setup import BaseTestCase
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings


class TestLoginEndpoint(BaseTestCase):
    """Test class for the login endpoint following test guide principles."""

    def setUp(self):
        super().setUp()
        self.login_url = "/api/v1/accounts/login/"

    def test_login_success(self):
        """Test successful login with valid credentials."""
        response = self.client.post(
            self.login_url,
            {
                "method": "password",
                "username": self.user.user.username,
                "password": "password123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Decode the refresh token to verify claims
        refresh_token = response.data["refresh"]
        decoded_refresh = RefreshToken(refresh_token)

        # Verify user data is embedded in the token claims
        self.assertEqual(decoded_refresh["email"], self.user.user.email)
        self.assertEqual(decoded_refresh["user_id"], self.user.user.id)
        self.assertEqual(decoded_refresh["profile_id"], self.user.id)
        self.assertEqual(decoded_refresh["role"], "user")  # Default role

        # Decode the access token to verify claims
        access_token = response.data["access"]
        # Use jwt.decode with options to skip verification for testing
        decoded_access = jwt.decode(
            access_token, options={"verify_signature": False, "verify_exp": False}
        )

        # Verify user data is also in the access token
        self.assertEqual(decoded_access["email"], self.user.user.email)
        self.assertEqual(decoded_access["user_id"], self.user.user.id)
        self.assertEqual(decoded_access["profile_id"], self.user.id)
        self.assertEqual(decoded_access["role"], "user")

    def test_login_invalid_credentials(self):
        """Test login failure with invalid credentials."""
        response = self.client.post(
            self.login_url,
            {
                "method": "password",
                "username": self.user.user.username,
                "password": "wrongpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["message"], "Invalid username or password")

    def test_login_user_not_found(self):
        """Test login failure when user does not exist."""
        response = self.client.post(
            self.login_url,
            {
                "method": "password",
                "username": "nonexistent",
                "password": "password123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["message"], "Invalid username or password")
