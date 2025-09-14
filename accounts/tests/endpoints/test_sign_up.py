from core.tests.setup import BaseTestCase
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from django.contrib.auth.models import User


class TestSignupEndpoint(BaseTestCase):
    """Test class for the signup endpoint following test guide principles."""

    def setUp(self):
        super().setUp()
        self.signup_url = "/api/v1/accounts/sign-up/"

    def test_signup_success(self):
        """Test successful signup with valid password method."""
        response = self.client.post(
            self.signup_url,
            {
                "method": "password",
                "email": "signup@email.com",
                "password": "newpassword123",
                "first_name": "Sibo",
                "last_name": "Alphonse",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Verify user was created in database
        new_user = User.objects.get(email="signup@email.com")
        self.assertEqual(new_user.first_name, "Sibo")
        self.assertEqual(new_user.last_name, "Alphonse")

        # Decode the refresh token to verify claims
        refresh_token = response.data["refresh"]
        decoded_refresh = RefreshToken(refresh_token)

        # Verify user data is embedded in the token claims
        self.assertEqual(decoded_refresh["email"], "signup@email.com")
        self.assertEqual(decoded_refresh["user_id"], new_user.id)
        self.assertEqual(decoded_refresh["profile_id"], new_user.userprofile.id)
        self.assertEqual(decoded_refresh["role"], "user")  # Default role

        # Decode the access token to verify claims
        access_token = response.data["access"]
        decoded_access = jwt.decode(
            access_token, options={"verify_signature": False, "verify_exp": False}
        )

        # Verify user data is also in the access token
        self.assertEqual(decoded_access["email"], "signup@email.com")
        self.assertEqual(decoded_access["user_id"], new_user.id)
        self.assertEqual(decoded_access["profile_id"], new_user.userprofile.id)
        self.assertEqual(decoded_access["role"], "user")

    def test_signup_duplicate_email(self):
        """Test signup failure with duplicate email."""
        response = self.client.post(
            self.signup_url,
            {
                "method": "password",
                "email": self.user.user.email,  # Use existing user's email
                "password": "newpassword123",
                "first_name": "Test",
                "last_name": "User",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["message"], "User with this email already exists"
        )

    def test_signup_weak_password(self):
        """Test signup failure with weak password."""
        response = self.client.post(
            self.signup_url,
            {
                "method": "password",
                "email": "test@example.com",
                "password": "123",  # Weak password
                "first_name": "Test",
                "last_name": "User",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        # Message will contain Django's password validation error

    def test_signup_missing_method(self):
        """Test signup failure when method is missing."""
        response = self.client.post(
            self.signup_url,
            {
                "email": "test@example.com",
                "password": "validpassword123",
                "first_name": "Test",
                "last_name": "User",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
