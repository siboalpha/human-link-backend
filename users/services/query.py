from core.data_classes import ServiceResponse
from users.models import UserProfile


class ProfileQueryService:
    def __init__(self):
        pass

    def getUserProfile(self, user_id) -> ServiceResponse:
        """
        Args:
            user_id (int): The ID of the user whose profile is to be retrieved.

        Business logic:
            1. Validate the user_id.
            2. Retrieve the user profile from the database.
            3. Return the user profile data.

        Returns:
            ServiceResponse: A response object containing success status, message, data (user profile), and status code.
        """
        try:
            profile = UserProfile.objects.get(user__id=user_id)
            profile_data = {
                "id": profile.id,
                "user_id": profile.user.id,
                "bio": profile.bio,
                "location": profile.location,
                "birth_date": profile.birth_date,
                "phone_number": profile.phone_number,
                "avatar": profile.avatar,
                "created_at": profile.created_at,
                "updated_at": profile.updated_at,
            }
            return ServiceResponse(
                success=True,
                message="User profile retrieved successfully",
                data=profile_data,
                status_code=200,
            )
        except UserProfile.DoesNotExist:
            return ServiceResponse(
                success=False, message="User profile not found", status_code=404
            )
