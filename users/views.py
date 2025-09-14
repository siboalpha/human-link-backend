from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.services.preferences_operations import PreferencesOperations
from users.services.preferences_query import PreferencesQuery
from users.services.preferences_utils import PreferencesUtils


# Initialize services
preferences_operations = PreferencesOperations()
preferences_query = PreferencesQuery()
preferences_utils = PreferencesUtils()


# User Preferences CRUD Views
@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def preferences_view(request):
    """Handle user preferences CRUD operations"""

    if request.method == "GET":
        # Get user's preferences
        service_response = preferences_operations.get_preferences(request.user)
        return Response(service_response.data, status=service_response.status_code)

    elif request.method == "POST":
        # Create new preferences
        service_response = preferences_operations.create_preferences(
            request.user, request.data
        )
        return Response(service_response.data, status=service_response.status_code)

    elif request.method in ["PUT", "PATCH"]:
        # Update preferences
        partial = request.method == "PATCH"
        service_response = preferences_operations.update_preferences(
            request.user, request.data, partial
        )
        return Response(service_response.data, status=service_response.status_code)

    elif request.method == "DELETE":
        # Delete preferences
        service_response = preferences_operations.delete_preferences(request.user)
        return Response(
            {"message": service_response.message}, status=service_response.status_code
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def preferences_status_view(request):
    """Get preferences completion status"""
    service_response = preferences_operations.get_preferences_status(request.user)
    return Response(service_response.data, status=service_response.status_code)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def preferences_section_update_view(request, section):
    """Update specific section of preferences"""
    service_response = preferences_utils.update_preferences_section(
        request.user, section, request.data
    )
    return Response(service_response.data, status=service_response.status_code)


# Preferences Query Views
@api_view(["GET"])
@permission_classes([AllowAny])
def preferences_choices_view(request):
    """Get all available choices for preferences fields"""
    service_response = preferences_query.get_preferences_choices()
    return Response(service_response.data, status=service_response.status_code)


@api_view(["GET"])
@permission_classes([AllowAny])
def preferences_sections_view(request):
    """Get preferences section definitions"""
    service_response = preferences_query.get_preferences_sections()
    return Response(service_response.data, status=service_response.status_code)


@api_view(["POST"])
@permission_classes([AllowAny])
def preferences_validate_view(request):
    """Validate preferences data without saving"""
    service_response = preferences_utils.validate_preferences_data(request.data)
    return Response(service_response.data, status=service_response.status_code)
