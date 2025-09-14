# User Preferences Operations Service
from core.utils.data_classes import ServiceResponse
from users.repositories.preferences_repository import PreferencesRepository
from users.serializers import UserCompatibilityPreferencesSerializer
from core.utils.logging import LoggingService
from django.utils import timezone


class PreferencesOperations:
    """
    Service layer for handling user preferences operations
    Returns ServiceResponse with serialized data for views
    """

    def __init__(self):
        self.repository = PreferencesRepository()
        self.logger = LoggingService()

    def get_preferences(self, user) -> ServiceResponse:
        """Get user's preferences"""
        try:
            # Get user profile
            if not hasattr(user, "userprofile"):
                return ServiceResponse(
                    success=False, message="User profile not found", status_code=404
                )

            profile = user.userprofile

            # Get preferences from repository
            repo_response = self.repository.get_preferences_by_profile_id(profile.id)

            if not repo_response.success:
                return ServiceResponse(
                    success=False, message="User preferences not found", status_code=404
                )

            # Serialize the preferences object
            serializer = UserCompatibilityPreferencesSerializer(repo_response.data)

            return ServiceResponse(
                success=True,
                message="User preferences retrieved successfully",
                data=serializer.data,
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error getting preferences: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while retrieving preferences",
                status_code=500,
            )

    def create_preferences(self, user, preferences_data) -> ServiceResponse:
        """Create new preferences for user"""
        try:
            # Get user profile
            if not hasattr(user, "userprofile"):
                return ServiceResponse(
                    success=False, message="User profile not found", status_code=404
                )

            profile = user.userprofile

            # Check if preferences already exist
            existing_response = self.repository.get_preferences_by_profile_id(
                profile.id
            )
            if existing_response.success:
                return ServiceResponse(
                    success=False,
                    message="User preferences already exist",
                    status_code=400,
                )

            # Validate data
            serializer = UserCompatibilityPreferencesSerializer(data=preferences_data)
            if not serializer.is_valid():
                return ServiceResponse(
                    success=False,
                    message="Invalid preferences data",
                    data={"errors": serializer.errors},
                    status_code=400,
                )

            # Create preferences through repository
            repo_response = self.repository.create_preferences(
                profile, serializer.validated_data
            )

            if not repo_response.success:
                return ServiceResponse(
                    success=False, message=repo_response.message, status_code=400
                )

            # Log the creation
            self.logger.log(f"User preferences created for user {user.username}")

            # Serialize the created preferences
            created_serializer = UserCompatibilityPreferencesSerializer(
                repo_response.data
            )

            return ServiceResponse(
                success=True,
                message="User preferences created successfully",
                data=created_serializer.data,
                status_code=201,
            )

        except Exception as e:
            self.logger.log(
                f"Error creating preferences: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while creating preferences",
                status_code=500,
            )

    def update_preferences(
        self, user, preferences_data, partial=True
    ) -> ServiceResponse:
        """Update user's preferences"""
        try:
            # Get user profile
            if not hasattr(user, "userprofile"):
                return ServiceResponse(
                    success=False, message="User profile not found", status_code=404
                )

            profile = user.userprofile

            # Get existing preferences or create if doesn't exist
            repo_response = self.repository.get_preferences_by_profile_id(profile.id)

            if not repo_response.success:
                # Create new preferences if none exist
                serializer = UserCompatibilityPreferencesSerializer(
                    data=preferences_data
                )
                if not serializer.is_valid():
                    return ServiceResponse(
                        success=False,
                        message="Invalid preferences data",
                        data={"errors": serializer.errors},
                        status_code=400,
                    )

                create_response = self.repository.create_preferences(
                    profile, serializer.validated_data
                )
                if not create_response.success:
                    return ServiceResponse(
                        success=False, message=create_response.message, status_code=400
                    )

                self.logger.log(f"User preferences created for user {user.username}")
                preferences = create_response.data
                status_code = 201
            else:
                # Update existing preferences
                preferences = repo_response.data

                # Validate update data
                serializer = UserCompatibilityPreferencesSerializer(
                    preferences, data=preferences_data, partial=partial
                )
                if not serializer.is_valid():
                    return ServiceResponse(
                        success=False,
                        message="Invalid preferences data",
                        data={"errors": serializer.errors},
                        status_code=400,
                    )

                # Update through repository
                update_response = self.repository.update_preferences(
                    preferences, serializer.validated_data
                )
                if not update_response.success:
                    return ServiceResponse(
                        success=False, message=update_response.message, status_code=400
                    )

                self.logger.log(f"User preferences updated for user {user.username}")
                preferences = update_response.data
                status_code = 200

            # Check completion and update if necessary
            completion_percentage = preferences.calculate_completion_percentage()
            if completion_percentage >= 80 and not preferences.is_complete:
                preferences.is_complete = True
                preferences.completed_at = timezone.now()
                preferences.save()

            # Serialize the final preferences
            final_serializer = UserCompatibilityPreferencesSerializer(preferences)

            return ServiceResponse(
                success=True,
                message="User preferences updated successfully",
                data=final_serializer.data,
                status_code=status_code,
            )

        except Exception as e:
            self.logger.log(
                f"Error updating preferences: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while updating preferences",
                status_code=500,
            )

    def delete_preferences(self, user) -> ServiceResponse:
        """Delete user's preferences"""
        try:
            # Get user profile
            if not hasattr(user, "userprofile"):
                return ServiceResponse(
                    success=False, message="User profile not found", status_code=404
                )

            profile = user.userprofile

            # Get preferences
            repo_response = self.repository.get_preferences_by_profile_id(profile.id)
            if not repo_response.success:
                return ServiceResponse(
                    success=False, message="User preferences not found", status_code=404
                )

            # Delete through repository
            delete_response = self.repository.delete_preferences(repo_response.data)
            if not delete_response.success:
                return ServiceResponse(
                    success=False, message=delete_response.message, status_code=500
                )

            self.logger.log(f"User preferences deleted for user {user.username}")

            return ServiceResponse(
                success=True,
                message="User preferences deleted successfully",
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error deleting preferences: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while deleting preferences",
                status_code=500,
            )

    def get_preferences_status(self, user) -> ServiceResponse:
        """Get preferences completion status"""
        try:
            # Get user profile
            if not hasattr(user, "userprofile"):
                return ServiceResponse(
                    success=False, message="User profile not found", status_code=404
                )

            profile = user.userprofile

            # Check if preferences exist
            repo_response = self.repository.get_preferences_by_profile_id(profile.id)

            if not repo_response.success:
                # No preferences exist
                return ServiceResponse(
                    success=True,
                    message="Preferences status retrieved",
                    data={
                        "preferences_exist": False,
                        "is_complete": False,
                        "completion_percentage": 0,
                        "completed_at": None,
                    },
                    status_code=200,
                )

            preferences = repo_response.data
            completion_percentage = preferences.calculate_completion_percentage()

            return ServiceResponse(
                success=True,
                message="Preferences status retrieved",
                data={
                    "preferences_exist": True,
                    "is_complete": preferences.is_complete,
                    "completion_percentage": completion_percentage,
                    "completed_at": preferences.completed_at,
                },
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error getting preferences status: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while getting preferences status",
                status_code=500,
            )
