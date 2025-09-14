from core.tests.setup import BaseTestCase
from accounts.services.auth import AuthenticationService
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.contrib.auth.models import User


class TestSignup(BaseTestCase):
    """Test class for the signup dispatcher method following test guide principles."""

    def setUp(self):
        super().setUp()
        self.auth_service = AuthenticationService()

    def test_signup_success_with_password(self):
        """Test successful signup with valid password method."""
        response = self.auth_service.signup(
            method="password",
            email="signup1@email.com",
            password="newpassword123",
            first_name="Sibo",
            last_name="Alphonse",
        )

        self.assertTrue(response.success)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.status_code, 201)

        # Verify user was created in database
        new_user = User.objects.get(email="signup1@email.com")
        self.assertEqual(new_user.first_name, "Sibo")
        self.assertEqual(new_user.last_name, "Alphonse")

        # Decode the refresh token to verify claims
        refresh_token = response.data["refresh"]
        decoded_refresh = RefreshToken(refresh_token)

        # Verify user data is embedded in the token claims
        self.assertEqual(decoded_refresh["email"], "signup1@email.com")
        self.assertEqual(decoded_refresh["user_id"], new_user.id)
        self.assertEqual(decoded_refresh["profile_id"], new_user.userprofile.id)
        self.assertEqual(decoded_refresh["role"], "user")  # Default role

        # Decode the access token to verify claims
        access_token = response.data["access"]
        decoded_access = jwt.decode(
            access_token, options={"verify_signature": False, "verify_exp": False}
        )

        # Verify user data is also in the access token
        self.assertEqual(decoded_access["email"], "signup1@email.com")
        self.assertEqual(decoded_access["user_id"], new_user.id)
        self.assertEqual(decoded_access["profile_id"], new_user.userprofile.id)
        self.assertEqual(decoded_access["role"], "user")

    def test_signup_duplicate_email(self):
        """Test signup failure with duplicate email."""
        response = self.auth_service.signup(
            method="password",
            email=self.user.user.email,  # Use existing user's email
            password="newpassword123",
            first_name="Test",
            last_name="User",
        )

        self.assertFalse(response.success)
        self.assertEqual(response.message, "User with this email already exists")
        self.assertEqual(response.status_code, 400)

    def test_signup_weak_password(self):
        """Test signup failure with weak password."""
        response = self.auth_service.signup(
            method="password",
            email="test@example.com",
            password="123",  # Weak password
            first_name="Test",
            last_name="User",
        )

        self.assertFalse(response.success)
        self.assertEqual(response.status_code, 400)
        # Message will contain Django's password validation error

    def test_signup_invalid_method(self):
        """Test signup failure with invalid method."""
        response = self.auth_service.signup(
            method="invalid_method",
            email="test@example.com",
            password="validpassword123",
        )

        self.assertFalse(response.success)
        self.assertEqual(
            response.message,
            "Invalid signup method. Use 'password', 'google', or 'facebook'",
        )
        self.assertEqual(response.status_code, 400)
