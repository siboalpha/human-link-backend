# Compatibility Preferences Repository
from core.utils.data_classes import RepositoryResponse
from users.models import UserCompatibilityPreferences, UserProfile
from django.core.exceptions import ValidationError
from django.db import transaction
from core.utils.logging import LoggingService


class CompatibilityPreferencesRepository:
    """
    Repository layer for handling compatibility preferences database operations
    Returns RepositoryResponse with raw objects/querysets
    """

    def __init__(self):
        self.logger = LoggingService()

    def get_preferences_by_profile_id(self, profile_id: int) -> RepositoryResponse:
        """Get compatibility preferences by profile ID"""
        try:
            preferences = UserCompatibilityPreferences.objects.get(
                profile_id=profile_id
            )
            return RepositoryResponse(
                success=True,
                message="Compatibility preferences found",
                data=preferences,
            )
        except UserCompatibilityPreferences.DoesNotExist:
            return RepositoryResponse(
                success=False, message="Compatibility preferences not found", data=None
            )
        except Exception as e:
            self.logger.log(
                f"Error getting compatibility preferences: {str(e)}",
                level="error",
                error=e,
            )
            return RepositoryResponse(
                success=False, message="Database error occurred", error=str(e)
            )

    def create_preferences(
        self, profile: UserProfile, preferences_data: dict
    ) -> RepositoryResponse:
        """Create new compatibility preferences for profile"""
        try:
            with transaction.atomic():
                preferences = UserCompatibilityPreferences.objects.create(
                    profile=profile, **preferences_data
                )
                return RepositoryResponse(
                    success=True,
                    message="Compatibility preferences created successfully",
                    data=preferences,
                )
        except ValidationError as e:
            return RepositoryResponse(
                success=False, message="Validation error", error=str(e)
            )
        except Exception as e:
            self.logger.log(
                f"Error creating compatibility preferences: {str(e)}",
                level="error",
                error=e,
            )
            return RepositoryResponse(
                success=False,
                message="Failed to create compatibility preferences",
                error=str(e),
            )

    def update_preferences(
        self, preferences: UserCompatibilityPreferences, update_data: dict
    ) -> RepositoryResponse:
        """Update existing compatibility preferences"""
        try:
            with transaction.atomic():
                for field, value in update_data.items():
                    if hasattr(preferences, field):
                        setattr(preferences, field, value)

                preferences.save()
                return RepositoryResponse(
                    success=True,
                    message="Compatibility preferences updated successfully",
                    data=preferences,
                )
        except ValidationError as e:
            return RepositoryResponse(
                success=False, message="Validation error", error=str(e)
            )
        except Exception as e:
            self.logger.log(
                f"Error updating compatibility preferences: {str(e)}",
                level="error",
                error=e,
            )
            return RepositoryResponse(
                success=False,
                message="Failed to update compatibility preferences",
                error=str(e),
            )

    def delete_preferences(
        self, preferences: UserCompatibilityPreferences
    ) -> RepositoryResponse:
        """Delete compatibility preferences"""
        try:
            with transaction.atomic():
                preferences.delete()
                return RepositoryResponse(
                    success=True,
                    message="Compatibility preferences deleted successfully",
                    data=None,
                )
        except Exception as e:
            self.logger.log(
                f"Error deleting compatibility preferences: {str(e)}",
                level="error",
                error=e,
            )
            return RepositoryResponse(
                success=False,
                message="Failed to delete compatibility preferences",
                error=str(e),
            )

    def get_preferences_choices(self) -> RepositoryResponse:
        """Get all available choices for compatibility preferences fields"""
        try:
            choices_data = {
                "gender_choices": UserCompatibilityPreferences.GENDER_CHOICES,
            }

            return RepositoryResponse(
                success=True,
                message="Choices retrieved successfully",
                data=choices_data,
            )
        except Exception as e:
            self.logger.log(
                f"Error getting preferences choices: {str(e)}", level="error", error=e
            )
            return RepositoryResponse(
                success=False, message="Failed to get preferences choices", error=str(e)
            )
