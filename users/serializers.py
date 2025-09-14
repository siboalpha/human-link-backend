from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserPreferences, UserCompatibilityPreferences


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = UserProfile

        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "email",
            "bio",
            "location",
            "birth_date",
            "phone_number",
            "avatar",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserPreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for the user preferences with completion percentage calculation
    """

    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserPreferences
        fields = [
            "id",
            # Section 1: Basic Demographics & Life Context
            "age_range",
            "current_location",
            "life_situations",
            "preferred_chat_times",
            "daily_routine_word",
            # Section 2: Interests & Hobbies
            "top_hobbies",
            "other_hobbies",
            "enjoyed_media",
            "media_favorites",
            "niche_interests",
            "free_day_preference",
            "recent_inspiration",
            "interested_in_learning",
            # Section 3: Personality & Behaviors
            "outgoing_scale",
            "stress_handling",
            "stress_handling_other",
            "personality_words",
            "conversation_style",
            "primary_motivation",
            "new_things_scale",
            # Section 4: Values & Communication Style
            "important_values",
            "communication_preference",
            "favorite_topics",
            "topics_to_avoid",
            "connection_frequency",
            "serious_conversation_response",
            # Section 5: Goals & Preferences
            "friendship_goals",
            "friend_preferences",
            "perfect_friendship_description",
            # Metadata
            "is_complete",
            "completed_at",
            "completion_percentage",
            "created_at",
            "updated_at",
        ]

    def get_completion_percentage(self, obj):
        return obj.calculate_completion_percentage()


UserQuestionnaireSerializer = UserPreferencesSerializer
UserQuestionnaireResponseSerializer = UserPreferencesSerializer


class UserCompatibilityPreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for user compatibility preferences and matching criteria
    """

    class Meta:
        model = UserCompatibilityPreferences
        fields = [
            "id",
            "preferred_age_range_min",
            "preferred_age_range_max",
            "preferred_gender",
            "geographic_preference",
            "hobby_importance",
            "personality_importance",
            "values_importance",
            "lifestyle_importance",
            "excluded_topics",
            "excluded_personalities",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserProfileWithPreferencesSerializer(serializers.ModelSerializer):
    """
    Extended user profile serializer that includes preferences data
    """

    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    preferences = UserPreferencesSerializer(source="preferences", read_only=True)
    compatibility_prefs = UserCompatibilityPreferencesSerializer(read_only=True)
    preferences_status = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "email",
            "bio",
            "location",
            "birth_date",
            "phone_number",
            "avatar",
            "email_verified",
            "preferences",
            "compatibility_prefs",
            "preferences_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "email_verified"]

    def get_preferences_status(self, obj):
        """Get preferences completion status"""
        if hasattr(obj, "preferences"):
            return {
                "completed": obj.preferences.is_complete,
                "completion_percentage": obj.preferences.calculate_completion_percentage(),
                "completed_at": obj.preferences.completed_at,
            }
        return {"completed": False, "completion_percentage": 0, "completed_at": None}


# Simplified serializer for preferences choices/options
class PreferencesChoicesSerializer(serializers.Serializer):
    """
    Serializer to provide all available choices for the preferences fields
    """

    age_choices = serializers.ListField()
    life_situation_choices = serializers.ListField()
    chat_time_choices = serializers.ListField()
    hobby_choices = serializers.ListField()
    media_choices = serializers.ListField()
    free_day_choices = serializers.ListField()
    stress_handling_choices = serializers.ListField()
    conversation_style_choices = serializers.ListField()
    motivation_choices = serializers.ListField()
    friendship_values_choices = serializers.ListField()
    communication_style_choices = serializers.ListField()
    connection_frequency_choices = serializers.ListField()
    serious_conversation_choices = serializers.ListField()
    friendship_goals_choices = serializers.ListField()
    friend_preferences_choices = serializers.ListField()


# Keep old name for backward compatibility
QuestionnaireChoicesSerializer = PreferencesChoicesSerializer
