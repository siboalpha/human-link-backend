from core.utils.data_classes import ServiceResponse
from users.models import UserProfile, UserPreferences
from users.serializers import UserPreferencesSerializer
from users.repositories.preferences_repository import PreferencesRepository


class PreferencesService:
    """
    Service layer for handling user preferences business logic
    Returns ServiceResponse with serialized data
    """

    @staticmethod
    def get_user_preferences(user):
        preferences = UserPreferences.objects.filter(user=user).first()
        # Remove or update compatibility preferences logic as needed

        if not preferences:
            return None

        return {
            "user_preferences": preferences,
        }

    def get_preferences_by_profile_id(self, profile_id: int) -> ServiceResponse:
        """Get user preferences by profile ID"""
        repo_response = PreferencesRepository.get_preferences_by_profile_id(profile_id)
        if not repo_response.success:
            return ServiceResponse(success=False, message=repo_response.message)
        serializer = UserPreferencesSerializer(repo_response.data)
        return ServiceResponse(success=True, data=serializer.data)

    def create_preferences(
        self, profile: UserProfile, preferences_data: dict
    ) -> ServiceResponse:
        """Create new user preferences"""
        repo_response = PreferencesRepository.create_preferences(
            profile, preferences_data
        )
        if not repo_response.success:
            return ServiceResponse(success=False, message=repo_response.message)
        serializer = UserPreferencesSerializer(repo_response.data)
        return ServiceResponse(success=True, data=serializer.data)

    def update_preferences(
        self, profile: UserProfile, update_data: dict
    ) -> ServiceResponse:
        """Update user preferences"""
        preferences_response = PreferencesRepository.get_preferences_by_profile_id(
            profile.id
        )
        if not preferences_response.success:
            return ServiceResponse(success=False, message=preferences_response.message)
        preferences = preferences_response.data
        repo_response = PreferencesRepository.update_preferences(
            preferences, update_data
        )
        if not repo_response.success:
            return ServiceResponse(success=False, message=repo_response.message)
        serializer = UserPreferencesSerializer(repo_response.data)
        return ServiceResponse(success=True, data=serializer.data)
