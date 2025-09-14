# User Preferences Utils Service
from core.utils.data_classes import ServiceResponse
from users.repositories.preferences_repository import PreferencesRepository
from users.serializers import UserPreferencesSerializer
from core.utils.logging import LoggingService
from django.utils import timezone


class PreferencesUtils:
    """
    Service layer for handling user preferences utility operations
    Returns ServiceResponse with processed data for views
    """

    def __init__(self):
        self.repository = PreferencesRepository()
        self.logger = LoggingService()

    def update_preferences_section(
        self, user, section: str, section_data: dict
    ) -> ServiceResponse:
        """Update a specific section of user preferences"""
        try:
            # Get user profile
            if not hasattr(user, "userprofile"):
                return ServiceResponse(
                    success=False, message="User profile not found", status_code=404
                )

            profile = user.userprofile

            # Validate section name
            valid_sections = [
                "demographics",
                "interests",
                "personality",
                "values",
                "goals",
            ]
            if section not in valid_sections:
                return ServiceResponse(
                    success=False,
                    message=f"Invalid section. Must be one of: {', '.join(valid_sections)}",
                    status_code=400,
                )

            # Map section to fields
            section_fields = {
                "demographics": [
                    "age_range",
                    "current_location",
                    "life_situations",
                    "preferred_chat_times",
                    "daily_routine_word",
                ],
                "interests": [
                    "top_hobbies",
                    "other_hobbies",
                    "enjoyed_media",
                    "media_favorites",
                    "niche_interests",
                    "free_day_preference",
                    "recent_inspiration",
                    "interested_in_learning",
                ],
                "personality": [
                    "outgoing_scale",
                    "stress_handling",
                    "stress_handling_other",
                    "personality_words",
                    "conversation_style",
                    "primary_motivation",
                    "new_things_scale",
                ],
                "values": [
                    "important_values",
                    "communication_preference",
                    "favorite_topics",
                    "topics_to_avoid",
                    "connection_frequency",
                    "serious_conversation_response",
                ],
                "goals": [
                    "friendship_goals",
                    "friend_preferences",
                    "perfect_friendship_description",
                ],
            }

            # Filter data to only include fields for this section
            filtered_data = {}
            for field in section_fields[section]:
                if field in section_data:
                    filtered_data[field] = section_data[field]

            # Get existing preferences or create if doesn't exist
            repo_response = self.repository.get_preferences_by_profile_id(profile.id)

            if not repo_response.success:
                # Create new preferences with section data
                serializer = UserPreferencesSerializer(data=filtered_data)
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
                # Update existing preferences with section data
                preferences = repo_response.data

                # Validate section data
                serializer = UserPreferencesSerializer(
                    preferences, data=filtered_data, partial=True
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

                self.logger.log(
                    f"User preferences section '{section}' updated for user {user.username}"
                )
                preferences = update_response.data
                status_code = 200

            # Check completion and update if necessary
            completion_percentage = preferences.calculate_completion_percentage()
            if completion_percentage >= 80 and not preferences.is_complete:
                preferences.is_complete = True
                preferences.completed_at = timezone.now()
                preferences.save()

            # Serialize the final preferences
            final_serializer = UserPreferencesSerializer(preferences)

            return ServiceResponse(
                success=True,
                message=f"Preferences section '{section}' updated successfully",
                data=final_serializer.data,
                status_code=status_code,
            )

        except Exception as e:
            self.logger.log(
                f"Error updating preferences section: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while updating preferences section",
                status_code=500,
            )

    def validate_preferences_data(self, preferences_data: dict) -> ServiceResponse:
        """Validate preferences data without saving to database"""
        try:
            # Use serializer to validate data
            serializer = UserPreferencesSerializer(data=preferences_data)

            if serializer.is_valid():
                return ServiceResponse(
                    success=True,
                    message="Preferences data is valid",
                    data={"valid": True, "validated_data": serializer.validated_data},
                    status_code=200,
                )
            else:
                return ServiceResponse(
                    success=False,
                    message="Invalid preferences data",
                    data={"valid": False, "errors": serializer.errors},
                    status_code=400,
                )

        except Exception as e:
            self.logger.log(
                f"Error validating preferences data: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while validating preferences data",
                status_code=500,
            )

    def calculate_compatibility_score(
        self, user1_preferences, user2_preferences
    ) -> ServiceResponse:
        """Calculate compatibility score between two users' preferences"""
        try:
            score = 0.0
            total_weight = 0.0

            # Define scoring weights for different categories
            weights = {
                "age_range": 0.1,
                "life_situations": 0.15,
                "top_hobbies": 0.2,
                "enjoyed_media": 0.1,
                "free_day_preference": 0.1,
                "conversation_style": 0.15,
                "communication_preference": 0.1,
                "friendship_goals": 0.1,
            }

            # Calculate weighted scores
            for field, weight in weights.items():
                user1_value = getattr(user1_preferences, field, None)
                user2_value = getattr(user2_preferences, field, None)

                if user1_value and user2_value:
                    total_weight += weight

                    if isinstance(user1_value, list) and isinstance(user2_value, list):
                        # For list fields, calculate overlap percentage
                        overlap = len(set(user1_value) & set(user2_value))
                        total_unique = len(set(user1_value + user2_value))
                        if total_unique > 0:
                            field_score = overlap / total_unique
                            score += field_score * weight
                    elif user1_value == user2_value:
                        # For exact matches
                        score += weight

            # Normalize score to percentage
            compatibility_percentage = (
                (score / total_weight * 100) if total_weight > 0 else 0
            )

            return ServiceResponse(
                success=True,
                message="Compatibility score calculated successfully",
                data={
                    "compatibility_percentage": round(compatibility_percentage, 2),
                    "factors_considered": list(weights.keys()),
                    "total_weight": total_weight,
                },
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error calculating compatibility score: {str(e)}",
                level="error",
                error=e,
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while calculating compatibility score",
                status_code=500,
            )
