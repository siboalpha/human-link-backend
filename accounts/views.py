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
    if method == "password":
        username = data.get("username")
        password = data.get("password")
        response = auth_service.loginWithPassword(username, password)

    elif method == "google":
        google_token = data.get("google_token")
        response = auth_service.loginWithGoogle(google_token)

    elif method == "facebook":
        facebook_token = data.get("facebook_token")
        response = auth_service.loginWithFacebook(facebook_token)

    else:
        return Response(
            {"error": "Invalid login method"}, status=status.HTTP_400_BAD_REQUEST
        )

    if not response:
        return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

    if not response.success:
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
