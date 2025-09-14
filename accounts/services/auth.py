# authentication class
from core.data_classes import ServiceResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from users.models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class AuthenticationService:
    def __init__(self):
        pass

    def signin(self, method, **kwargs) -> ServiceResponse:
        """
        Args:
            method (str): The signin method ('password', 'google', 'facebook').
            **kwargs: Additional parameters required for the specific signin method.
        Business logic:
            1. Depending on the method, call the appropriate signin function.
            2. For password signin, validate username and password, authenticate user.
            3. For Google/Facebook signin, validate token, retrieve user info, authenticate user.
        Returns:
            ServiceResponse: A response object containing success status, message, data (tokens), and status code.
        """
        if method == "password":
            username = kwargs.get("username")
            password = kwargs.get("password")
            return self.signinWithPassword(username, password)

        elif method == "google":
            google_token = kwargs.get("google_token")
            return self.signinWithGoogle(google_token)

        elif method == "facebook":
            facebook_token = kwargs.get("facebook_token")
            return self.signinWithFacebook(facebook_token)

        else:
            return ServiceResponse(
                success=False,
                message="Invalid signin method. Use 'password', 'google', or 'facebook'",
                status_code=400,
            )

    def signinWithPassword(self, username, password) -> ServiceResponse:
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

        # Add custom claims to the token
        refresh["email"] = user.email
        refresh["user_id"] = user.id
        refresh["role"] = getattr(user, "role", "user")

        # Get profile ID if user has a profile
        if hasattr(user, "userprofile"):
            refresh["profile_id"] = user.userprofile.id

        # Prepare response data with only tokens
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return ServiceResponse(
            success=True,
            message="signin successful",
            data=response_data,
            status_code=200,
        )

    def signinWithGoogle(self, google_token) -> ServiceResponse:
        # Implement Google signin logic here
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

    def signinWithFacebook(self, facebook_token) -> ServiceResponse:
        # Implement Facebook signin logic here
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

    def signup(self, method, **kwargs) -> ServiceResponse:
        """
        Args:
            method (str): The registration method ('password', 'google', 'facebook').
            **kwargs: Additional parameters required for the specific registration method.
        Business logic:
            1. Depending on the method, call the appropriate registration function.
            2. For password registration, validate email and password, create user.
            3. For Google/Facebook registration, validate token, retrieve user info, create user if not exists.
        Returns:
            ServiceResponse: A response object containing success status, message, data (user info), and status code.
        """
        if method == "password":
            email = kwargs.get("email")
            password = kwargs.get("password")
            extra_fields = {
                k: v for k, v in kwargs.items() if k not in ["email", "password"]
            }
            return self.signupWithPassword(email, password, **extra_fields)

        elif method == "google":
            google_token = kwargs.get("google_token")
            extra_fields = {k: v for k, v in kwargs.items() if k != "google_token"}
            return self.signupWithGoogle(google_token, **extra_fields)

        elif method == "facebook":
            facebook_token = kwargs.get("facebook_token")
            extra_fields = {k: v for k, v in kwargs.items() if k != "facebook_token"}
            return self.signupWithFacebook(facebook_token, **extra_fields)

        else:
            return ServiceResponse(
                success=False,
                message="Invalid signup method. Use 'password', 'google', or 'facebook'",
                status_code=400,
            )

    def signupWithPassword(self, email, password, **extra_fields) -> ServiceResponse:
        """
        Args:
            email (str): The email address of the user.
            password (str): The password for the account.
            **extra_fields: Additional fields for user creation (e.g., first_name, last_name).
        Business logic:
            1. Validate the email format and password strength.
            2. Check if the email already exists in the database.
            3. Create a new user with the provided email, password, and extra fields.
            4. Create a user profile for the new user.
            5. Generate JWT tokens with embedded claims.
        Returns:
            ServiceResponse: A response object containing success status, message, data (tokens), and status code.
        """

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return ServiceResponse(
                success=False,
                message="User with this email already exists",
                status_code=400,
            )

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            return ServiceResponse(success=False, message=str(e), status_code=400)

        # Create user
        try:
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,
                **extra_fields,
            )

            # Create user profile
            profile = UserProfile.objects.create(user=user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Add custom claims to the token
            refresh["email"] = user.email
            refresh["user_id"] = user.id
            refresh["role"] = getattr(user, "role", "user")
            refresh["profile_id"] = profile.id

            # Prepare response data with only tokens
            response_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return ServiceResponse(
                success=True,
                message="User created successfully",
                data=response_data,
                status_code=201,
            )

        except Exception as e:
            return ServiceResponse(
                success=False, message=f"Error creating user: {str(e)}", status_code=500
            )

    def signupWithGoogle(self, google_token, **extra_fields) -> ServiceResponse:
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

    def signupWithFacebook(self, facebook_token, **extra_fields) -> ServiceResponse:
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
        pass
