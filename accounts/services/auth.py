# authentication class
from core.utils.data_classes import ServiceResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from users.models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from core.utils.logging import LoggingService
from accounts.utils.generate_token import TokenGenerator
from accounts.utils.emails import AccountEmails
from django.utils import timezone
from django.conf import settings


class AuthenticationService:
    def __init__(self):
        self.logger = LoggingService()
        self.token_generator = TokenGenerator()
        self.email_service = AccountEmails()

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
        try:
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
        except Exception as e:
            self.logger.log(f"Error during signin: {str(e)}", level="error", error=e)
            return ServiceResponse(
                success=False,
                message="An error occurred during signin",
                status_code=500,
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
        try:
            # Validate the username and password
            user = authenticate(username=username, password=password)
            if user is None:
                return ServiceResponse(
                    success=False,
                    message="Invalid username or password",
                    status_code=401,
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
        except Exception as e:
            self.logger.log(
                f"Error during password signin: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred during signin",
                status_code=500,
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
        try:
            # Check if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Don't reveal if email exists for security
                return ServiceResponse(
                    success=True,
                    message="If this email exists, a password reset link has been sent",
                    status_code=200,
                )

            # Generate password reset token
            reset_token = self.token_generator.generate_password_reset_token(user.id)

            # Create reset link (you'll need to adjust the frontend URL)
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

            # Send password reset email
            first_name = user.first_name or "User"
            email_sent = self.email_service.send_password_reset_email(
                to_email=user.email, first_name=first_name, reset_link=reset_link
            )

            if not email_sent:
                self.logger.log(
                    f"Failed to send password reset email to {email}", level="error"
                )
                return ServiceResponse(
                    success=False,
                    message="Failed to send password reset email",
                    status_code=500,
                )

            self.logger.log(f"Password reset email sent to {email}", level="info")
            return ServiceResponse(
                success=True,
                message="If this email exists, a password reset link has been sent",
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error during password reset for {email}: {str(e)}",
                level="error",
                error=e,
            )
            return ServiceResponse(
                success=False,
                message="An error occurred during password reset",
                status_code=500,
            )

    def confirmPasswordReset(self, token: str, new_password: str) -> ServiceResponse:
        """
        Confirm password reset with token and set new password.

        Args:
            token (str): The password reset token.
            new_password (str): The new password to set.

        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """
        try:
            # Verify the token
            payload = self.token_generator.verify_token(token, "password_reset")

            if "error" in payload:
                return ServiceResponse(
                    success=False,
                    message=payload["error"],
                    status_code=400,
                )

            # Get user
            user_id = payload.get("user_id")
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return ServiceResponse(
                    success=False,
                    message="Invalid token",
                    status_code=400,
                )

            # Validate new password
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return ServiceResponse(
                    success=False,
                    message=str(e),
                    status_code=400,
                )

            # Set new password
            user.set_password(new_password)
            user.save()

            self.logger.log(
                f"Password reset completed for user {user.email}", level="info"
            )
            return ServiceResponse(
                success=True,
                message="Password reset successfully",
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error during password reset confirmation: {str(e)}",
                level="error",
                error=e,
            )
            return ServiceResponse(
                success=False,
                message="An error occurred during password reset",
                status_code=500,
            )

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
        try:
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
                extra_fields = {
                    k: v for k, v in kwargs.items() if k != "facebook_token"
                }
                return self.signupWithFacebook(facebook_token, **extra_fields)

            else:
                return ServiceResponse(
                    success=False,
                    message="Invalid signup method. Use 'password', 'google', or 'facebook'",
                    status_code=400,
                )
        except Exception as e:
            self.logger.log(f"Error during signup: {str(e)}", level="error", error=e)
            return ServiceResponse(
                success=False,
                message="An error occurred during signup",
                status_code=500,
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
            5. Generate and send email verification token.
            6. Generate JWT tokens with embedded claims.
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

            # Generate email verification token
            verification_token = self.token_generator.generate_email_verification_token(
                user.id
            )

            # Save verification token to profile
            profile.email_verification_token = verification_token
            profile.email_verification_sent_at = timezone.now()
            profile.save()

            # Send verification email
            verification_link = (
                f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
            )
            first_name = user.first_name or "User"

            email_sent = self.email_service.send_email_verification(
                to_email=user.email,
                first_name=first_name,
                verification_link=verification_link,
            )

            if not email_sent:
                self.logger.log(
                    f"Failed to send verification email to {email}", level="warning"
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Add custom claims to the token
            refresh["email"] = user.email
            refresh["user_id"] = user.id
            refresh["role"] = getattr(user, "role", "user")
            refresh["profile_id"] = profile.id
            refresh["email_verified"] = profile.email_verified

            # Prepare response data with only tokens
            response_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email_verification_sent": email_sent,
            }

            self.logger.log(f"User created successfully: {email}", level="info")

            return ServiceResponse(
                success=True,
                message="User created successfully. Please check your email to verify your account.",
                data=response_data,
                status_code=201,
            )

        except Exception as e:
            self.logger.log(f"Error creating user: {str(e)}", level="error", error=e)
            return ServiceResponse(
                success=False,
                message="An error occurred while creating the user",
                status_code=500,
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

    def verifyEmail(self, token: str) -> ServiceResponse:
        """
        Args:
            token (str): The email verification token.
        Business logic:
            1. Decode and validate the verification token.
            2. Check if the token matches the one stored for the user.
            3. If it matches, mark the user's email as verified in the database.
        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """
        try:
            # Verify the token
            payload = self.token_generator.verify_token(token, "email_verification")

            if "error" in payload:
                return ServiceResponse(
                    success=False,
                    message=payload["error"],
                    status_code=400,
                )

            # Get user
            user_id = payload.get("user_id")
            try:
                user = User.objects.get(id=user_id)
                profile = user.userprofile
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return ServiceResponse(
                    success=False,
                    message="Invalid verification token",
                    status_code=400,
                )

            # Check if email is already verified
            if profile.email_verified:
                return ServiceResponse(
                    success=True,
                    message="Email already verified",
                    status_code=200,
                )

            # Verify the stored token matches
            if profile.email_verification_token != token:
                return ServiceResponse(
                    success=False,
                    message="Invalid verification token",
                    status_code=400,
                )

            # Mark email as verified
            profile.email_verified = True
            profile.email_verification_token = None  # Clear the token
            profile.save()

            self.logger.log(
                f"Email verified successfully for user {user.email}", level="info"
            )
            return ServiceResponse(
                success=True,
                message="Email verified successfully",
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error during email verification: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred during email verification",
                status_code=500,
            )

    def sendVerificationEmail(self, user) -> ServiceResponse:
        """
        Args:
            user (User): The user to send the verification email to.
        Business logic:
            1. Generate a verification token.
            2. Send an email to the user's email address with the verification link.
        Returns:
            ServiceResponse: A response object containing success status, message, and status code.
        """
        try:
            # Generate new verification token
            verification_token = self.token_generator.generate_email_verification_token(
                user.id
            )

            # Update profile with new token
            profile = user.userprofile
            profile.email_verification_token = verification_token
            profile.email_verification_sent_at = timezone.now()
            profile.save()

            # Send verification email
            verification_link = (
                f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
            )
            first_name = user.first_name or "User"

            email_sent = self.email_service.send_email_verification(
                to_email=user.email,
                first_name=first_name,
                verification_link=verification_link,
            )

            if not email_sent:
                return ServiceResponse(
                    success=False,
                    message="Failed to send verification email",
                    status_code=500,
                )

            self.logger.log(f"Verification email sent to {user.email}", level="info")
            return ServiceResponse(
                success=True,
                message="Verification email sent successfully",
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error sending verification email: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while sending verification email",
                status_code=500,
            )
