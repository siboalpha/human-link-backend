from core.tests.setup import BaseTestCase
from accounts.services.auth import AuthenticationService
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings


class TestSignin(BaseTestCase):
    """Test class for the signin dispatcher method following test guide principles."""

    def setUp(self):
        super().setUp()
        self.auth_service = AuthenticationService()

    def test_signin_success_with_password(self):
        """Test successful signin with valid password method."""
        response = self.auth_service.signin(
            method="password", username=self.user.user.username, password="password123"
        )
        self.assertTrue(response.success)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.status_code, 200)

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
        decoded_access = jwt.decode(
            access_token, options={"verify_signature": False, "verify_exp": False}
        )

        # Verify user data is also in the access token
        self.assertEqual(decoded_access["email"], self.user.user.email)
        self.assertEqual(decoded_access["user_id"], self.user.user.id)
        self.assertEqual(decoded_access["profile_id"], self.user.id)
        self.assertEqual(decoded_access["role"], "user")

    def test_signin_invalid_credentials(self):
        """Test signin failure with invalid credentials."""
        response = self.auth_service.signin(
            method="password",
            username=self.user.user.username,
            password="wrongpassword",
        )
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Invalid username or password")
        self.assertEqual(response.status_code, 401)

    def test_signin_user_not_found(self):
        """Test signin failure when user does not exist."""
        response = self.auth_service.signin(
            method="password", username="nonexistent", password="password123"
        )
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Invalid username or password")
        self.assertEqual(response.status_code, 401)

    def test_signin_invalid_method(self):
        """Test signin failure with invalid method."""
        response = self.auth_service.signin(
            method="invalid_method",
            username=self.user.user.username,
            password="password123",
        )
        self.assertFalse(response.success)
        self.assertEqual(
            response.message,
            "Invalid signin method. Use 'password', 'google', or 'facebook'",
        )
        self.assertEqual(response.status_code, 400)
