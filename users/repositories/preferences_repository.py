# User Preferences Repository
from core.utils.data_classes import RepositoryResponse
from users.models import UserProfile, UserPreferences
from users.serializers import UserPreferencesSerializer
from django.core.exceptions import ValidationError
from django.db import transaction
from core.utils.logging import LoggingService


class PreferencesRepository:
    """
    Repository layer for handling user preferences database operations
    Returns RepositoryResponse with raw objects/querysets
    """

    def __init__(self):
        self.logger = LoggingService()

    def get_preferences_by_profile_id(self, profile_id: int) -> RepositoryResponse:
        """Get preferences by profile ID"""
        try:
            preferences = UserPreferences.objects.get(profile_id=profile_id)
            return RepositoryResponse(
                success=True, message="User preferences found", data=preferences
            )
        except UserPreferences.DoesNotExist:
            return RepositoryResponse(
                success=False, message="User preferences not found", data=None
            )
        except Exception as e:
            self.logger.log(
                f"Error getting preferences: {str(e)}", level="error", error=e
            )
            return RepositoryResponse(
                success=False, message="Database error occurred", error=str(e)
            )

    def create_preferences(
        self, profile: UserProfile, preferences_data: dict
    ) -> RepositoryResponse:
        """Create new preferences for profile"""
        try:
            with transaction.atomic():
                preferences = UserPreferences.objects.create(
                    profile=profile, **preferences_data
                )
                return RepositoryResponse(
                    success=True,
                    message="User preferences created successfully",
                    data=preferences,
                )
        except ValidationError as e:
            return RepositoryResponse(
                success=False, message="Validation error", error=str(e)
            )
        except Exception as e:
            self.logger.log(
                f"Error creating preferences: {str(e)}", level="error", error=e
            )
            return RepositoryResponse(
                success=False, message="Failed to create preferences", error=str(e)
            )

    def update_preferences(
        self, preferences: UserPreferences, update_data: dict
    ) -> RepositoryResponse:
        """Update existing preferences"""
        try:
            with transaction.atomic():
                for field, value in update_data.items():
                    if hasattr(preferences, field):
                        setattr(preferences, field, value)

                preferences.save()
                return RepositoryResponse(
                    success=True,
                    message="User preferences updated successfully",
                    data=preferences,
                )
        except ValidationError as e:
            return RepositoryResponse(
                success=False, message="Validation error", error=str(e)
            )
        except Exception as e:
            self.logger.log(
                f"Error updating preferences: {str(e)}", level="error", error=e
            )
            return RepositoryResponse(
                success=False, message="Failed to update preferences", error=str(e)
            )

    def delete_preferences(self, preferences: UserPreferences) -> RepositoryResponse:
        """Delete preferences"""
        try:
            with transaction.atomic():
                preferences.delete()
                return RepositoryResponse(
                    success=True,
                    message="User preferences deleted successfully",
                    data=None,
                )
        except Exception as e:
            self.logger.log(
                f"Error deleting preferences: {str(e)}", level="error", error=e
            )
            return RepositoryResponse(
                success=False, message="Failed to delete preferences", error=str(e)
            )

    def get_preferences_choices(self) -> RepositoryResponse:
        """Get all available choices for preferences fields"""
        try:
            choices_data = {
                "age_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.AGE_CHOICES
                ],
                "life_situation_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.LIFE_SITUATION_CHOICES
                ],
                "chat_time_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.CHAT_TIME_CHOICES
                ],
                "hobby_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.HOBBY_CHOICES
                ],
                "media_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.MEDIA_CHOICES
                ],
                "free_day_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.FREE_DAY_CHOICES
                ],
                "stress_handling_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.STRESS_HANDLING_CHOICES
                ],
                "conversation_style_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.CONVERSATION_STYLE_CHOICES
                ],
                "motivation_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.MOTIVATION_CHOICES
                ],
                "friendship_values_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.FRIENDSHIP_VALUES_CHOICES
                ],
                "communication_style_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.COMMUNICATION_STYLE_CHOICES
                ],
                "connection_frequency_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.CONNECTION_FREQUENCY_CHOICES
                ],
                "serious_conversation_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.SERIOUS_CONVERSATION_CHOICES
                ],
                "friendship_goals_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.FRIENDSHIP_GOALS_CHOICES
                ],
                "friend_preferences_choices": [
                    {"value": choice[0], "label": choice[1]}
                    for choice in UserPreferences.FRIEND_PREFERENCES_CHOICES
                ],
            }

            return RepositoryResponse(
                success=True,
                message="Preferences choices retrieved successfully",
                data=choices_data,
            )
        except Exception as e:
            self.logger.log(
                f"Error getting preferences choices: {str(e)}", level="error", error=e
            )
            return RepositoryResponse(
                success=False, message="Failed to get preferences choices", error=str(e)
            )
