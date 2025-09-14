# auth views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.services.auth import AuthenticationService

auth_service = AuthenticationService()


# login view
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    data = request.data
    method = data.get("method")
    response = None

    # Check for valid login methods
    if method not in ["password", "email", "google", "facebook"]:
        return Response(
            {"message": "Invalid login method"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif method == "password":
        # Handle both username and email parameters for password login
        username = data.get("username") or data.get("email")
        password = data.get("password")

        response = auth_service.signin(
            method=method,
            username=username,
            password=password,
        )

    if not response or not response.success:
        return Response({"message": response.message}, status=response.status_code)
    return Response(response.data, status=response.status_code)


# signup view
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):

    data = request.data
    method = data.get("method")
    response = auth_service.signup(
        method=method,
        email=data.get("email"),
        password=data.get("password"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
    )
    if not response.success:
        return Response({"message": response.message}, status=response.status_code)
    return Response(response.data, status=response.status_code)


# Email verification view
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email_view(request):
    """Verify user's email with token"""
    data = request.data
    token = data.get("token")

    if not token:
        return Response(
            {"message": "Token is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = auth_service.verifyEmail(token)

    if not response.success:
        return Response({"message": response.message}, status=response.status_code)
    return Response({"message": response.message}, status=response.status_code)


# Resend verification email view
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def resend_verification_email_view(request):
    """Resend verification email to authenticated user"""
    user = request.user

    # Check if email is already verified
    if hasattr(user, "userprofile") and user.userprofile.email_verified:
        return Response(
            {"message": "Email is already verified"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = auth_service.sendVerificationEmail(user)

    if not response.success:
        return Response({"message": response.message}, status=response.status_code)
    return Response({"message": response.message}, status=response.status_code)


# Password reset request view
@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """Request password reset for given email"""
    data = request.data
    email = data.get("email")

    if not email:
        return Response(
            {"message": "Email is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = auth_service.resetPassword(email)

    if not response.success:
        return Response({"message": response.message}, status=response.status_code)
    return Response({"message": response.message}, status=response.status_code)


# Password reset confirmation view
@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    """Confirm password reset with token and new password"""
    data = request.data
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return Response(
            {"message": "Token and new password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = auth_service.confirmPasswordReset(token, new_password)

    if not response.success:
        return Response({"message": response.message}, status=response.status_code)
    return Response({"message": response.message}, status=response.status_code)
