# User Preferences Query Service
from core.utils.data_classes import ServiceResponse
from users.repositories.preferences_repository import PreferencesRepository
from core.utils.logging import LoggingService


class PreferencesQuery:
    """
    Service layer for handling user preferences query operations
    Returns ServiceResponse with formatted data for views
    """

    def __init__(self):
        self.repository = PreferencesRepository()
        self.logger = LoggingService()

    def get_preferences_choices(self) -> ServiceResponse:
        """Get all available choices for preferences fields"""
        try:
            repo_response = self.repository.get_preferences_choices()

            if not repo_response.success:
                return ServiceResponse(
                    success=False, message=repo_response.message, status_code=500
                )

            return ServiceResponse(
                success=True,
                message="Preferences choices retrieved successfully",
                data=repo_response.data,
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error getting preferences choices: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while retrieving preferences choices",
                status_code=500,
            )

    def get_preferences_sections(self) -> ServiceResponse:
        """Get preferences section definitions for dynamic forms"""
        try:
            sections_data = {
                "demographics": {
                    "title": "Basic Demographics & Life Context",
                    "description": "Tell us about your current life situation and preferences",
                    "fields": [
                        "age_range",
                        "current_location",
                        "life_situations",
                        "preferred_chat_times",
                        "daily_routine_word",
                    ],
                },
                "interests": {
                    "title": "Interests & Hobbies",
                    "description": "Share what you love to do in your free time",
                    "fields": [
                        "top_hobbies",
                        "other_hobbies",
                        "enjoyed_media",
                        "media_favorites",
                        "niche_interests",
                        "free_day_preference",
                        "recent_inspiration",
                        "interested_in_learning",
                    ],
                },
                "personality": {
                    "title": "Personality & Behaviors",
                    "description": "Help us understand your personality and how you handle different situations",
                    "fields": [
                        "outgoing_scale",
                        "stress_handling",
                        "stress_handling_other",
                        "personality_words",
                        "conversation_style",
                        "primary_motivation",
                        "new_things_scale",
                    ],
                },
                "values": {
                    "title": "Values & Communication Style",
                    "description": "Share what's important to you in relationships and how you like to communicate",
                    "fields": [
                        "important_values",
                        "communication_preference",
                        "favorite_topics",
                        "topics_to_avoid",
                        "connection_frequency",
                        "serious_conversation_response",
                    ],
                },
                "goals": {
                    "title": "Goals & Preferences",
                    "description": "Tell us what you're looking for in friendships and connections",
                    "fields": [
                        "friendship_goals",
                        "friend_preferences",
                        "perfect_friendship_description",
                    ],
                },
            }

            return ServiceResponse(
                success=True,
                message="Preferences sections retrieved successfully",
                data=sections_data,
                status_code=200,
            )

        except Exception as e:
            self.logger.log(
                f"Error getting preferences sections: {str(e)}", level="error", error=e
            )
            return ServiceResponse(
                success=False,
                message="An error occurred while retrieving preferences sections",
                status_code=500,
            )
