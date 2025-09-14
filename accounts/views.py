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
