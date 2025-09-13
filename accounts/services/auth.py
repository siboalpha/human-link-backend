# authentication class
from core.data_classes import ServiceResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from users.services.query import ProfileQueryService

profile_service = ProfileQueryService()


class AuthenticationService:
    def __init__(self):
        pass

    def login(self, method, **kwargs) -> ServiceResponse:
        pass

    def loginWithPassword(self, username, password) -> ServiceResponse:
        """
        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Business logic:
            1. Validate the username and password.
            2. Authenticate the user.
            3. Generate a token using jwt.
            4. Add email, user_id, profileId, role to token claims.
            5. Return refresh and access tokens.

        Returns:
            ServiceResponse: A response object containing success status, message, data (tokens), and status code.
        """
        # Validate the username and password
        user = authenticate(username=username, password=password)
        if user is None:
            return ServiceResponse(
                success=False, message="Invalid username or password", status_code=401
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # Add additional claims to the token
        tokens["email"] = user.email
        tokens["user_id"] = user.id

        # get users group as a role
        roles = user.groups.values_list("name", flat=True)
        tokens["roles"] = roles

        # get user profile id
        profile_response = profile_service.getUserProfile(user.id)
        if profile_response.success and profile_response.data:
            tokens["profile_id"] = profile_response.data["id"]
        else:
            tokens["profile_id"] = None

        return ServiceResponse(
            success=True, message="Login successful", data=tokens, status_code=200
        )

    def loginWithGoogle(self, google_token) -> ServiceResponse:
        # Implement Google login logic here
        """
        Args:
            google_token (str): The Google OAuth token.
        Business logic:
            1. Validate the Google token.
            2. Retrieve user information from Google.
            3. Check if the user exists in the database; if not, create a new user.
            4. Generate a token using jwt.
            5. Add email, user_id, profileId, role to token claims.
            6. Return refresh and access tokens.
        Returns:
            ServiceResponse: A response object containing success status, message, data (tokens), and status code.
        """

    def loginWithFacebook(self, facebook_token) -> ServiceResponse:
        # Implement Facebook login logic here
        """
        Args:
            facebook_token (str): The Facebook OAuth token.
        Business logic:
            1. Validate the Facebook token.
            2. Retrieve user information from Facebook.
            3. Check if the user exists in the database; if not, create a new user.
            4. Generate a token using jwt.
            5. Add email, user_id, profileId, role to token claims.
            6. Return refresh and access tokens.
        Returns:
            ServiceResponse: A response object containing success status, message, data (tokens), and status code.
        """

    def logout(self, user) -> ServiceResponse:
        # Implement logout logic here
        """
        Args:
            user (User): The user to log out.
        Business logic:
            1. Invalidate the user's token (if using token blacklisting).
            2. Perform any necessary cleanup actions.
        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """

    def resetPassword(self, email) -> ServiceResponse:
        # Implement password reset logic here
        """
        Args:
            email (str): The email of the user requesting a password reset.
        Business logic:
            1. Verify that the email exists in the database.
            2. Generate a password reset token.
            3. Send a password reset email to the user with the token.
        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """

    def changePassword(self, user, old_password, new_password) -> ServiceResponse:
        # Implement password change logic here
        """
        Args:
            user (User): The user requesting the password change.
            old_password (str): The user's current password.
            new_password (str): The new password to set.
        Business logic:
            1. Verify that the old password is correct.
            2. Validate the new password (e.g., check complexity requirements).
            3. Update the user's password in the database.
        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """

    def register(self, method, **kwargs) -> ServiceResponse:
        # Implement user registration logic here
        """
        Args:
            method (str): The registration method ('email', 'google', 'facebook').
            **kwargs: Additional parameters required for the specific registration method.
        Business logic:
            1. Depending on the method, call the appropriate registration function.
            2. For email registration, validate email and password, create user, send verification email.
            3. For Google/Facebook registration, validate token, retrieve user info, create user if not exists.
        Returns:
            ServiceResponse: A response object containing success status, message, data (user info), and status code.
        """

    def registerWithEmail(self, email, password, **extra_fields) -> ServiceResponse:
        # Implement email registration logic here
        """
        Args:
            email (str): The email address of the user.
            password (str): The password for the account.
            **extra_fields: Additional fields for user creation (e.g., first_name, last_name).
        Business logic:
            1. Validate the email format and password strength.
            2. Check if the email already exists in the database.
            3. Create a new user with the provided email, password, and extra fields.
            4. Send a verification email to the user.
        Returns:
            ServiceResponse: A response object containing success status, message, data (user info), and status code.
        """

    def registerWithGoogle(self, google_token, **extra_fields) -> ServiceResponse:
        # Implement Google registration logic here
        """
        Args:
            google_token (str): The Google OAuth token.
            **extra_fields: Additional fields for user creation (e.g., first_name, last_name).
        Business logic:
            1. Validate the Google token.
            2. Retrieve user information from Google.
            3. Check if the user exists in the database; if not, create a new user with extra fields.
            4. Send a verification email to the user if necessary.
        Returns:
            ServiceResponse: A response object containing success status, message, data (user info), and status code.
        """

    def registerWithFacebook(self, facebook_token, **extra_fields) -> ServiceResponse:
        # Implement Facebook registration logic here
        """
        Args:
            facebook_token (str): The Facebook OAuth token.
            **extra_fields: Additional fields for user creation (e.g., first_name, last_name).
        Business logic:
            1. Validate the Facebook token.
            2. Retrieve user information from Facebook.
            3. Check if the user exists in the database; if not, create a new user with extra fields.
            4. Send a verification email to the user if necessary.
        Returns:
            ServiceResponse: A response object containing success status, message, data (user info), and status code.
        """

    def verifyEmail(self, user, verification_code) -> ServiceResponse:
        # Implement email verification logic here
        """
        Args:
            user (User): The user to verify.
            verification_code (str): The verification code sent to the user's email.
        Business logic:
            1. Check if the verification code matches the one stored for the user.
            2. If it matches, mark the user's email as verified in the database.
        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """

    def sendVerificationEmail(self, user) -> ServiceResponse:
        # Implement sending verification email logic here
        """
        Args:
            user (User): The user to send the verification email to.
        Business logic:
            1. Generate a verification code or link.
            2. Send an email to the user's email address with the verification code/link.
        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """
