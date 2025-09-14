from django.db import models

from core.models import BaseModel


# Create your models here.
class UserProfile(BaseModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    # Email verification fields
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=500, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name if self.user.first_name else ''} {self.user.last_name if self.user.last_name else self.user.username}"


class UserPreferences(BaseModel):
    """
    Questionnaire model to capture user preferences and personality traits
    based on the Questionnaire.md specifications
    """

    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="questionnaire"
    )

    # Section 1: Basic Demographics & Life Context
    AGE_CHOICES = [
        ("18-24", "18-24"),
        ("25-34", "25-34"),
        ("35-44", "35-44"),
        ("45-54", "45-54"),
        ("55+", "55+"),
    ]
    age_range = models.CharField(
        max_length=10, choices=AGE_CHOICES, blank=True, null=True
    )
    current_location = models.CharField(max_length=200, blank=True, null=True)

    LIFE_SITUATION_CHOICES = [
        ("student", "Student"),
        ("working_professional", "Working Professional"),
        ("parent", "Parent"),
        ("retiree", "Retiree"),
        ("remote_worker", "Remote Worker"),
    ]
    life_situations = models.JSONField(default=list, blank=True)

    CHAT_TIME_CHOICES = [
        ("mornings", "Mornings"),
        ("evenings", "Evenings"),
        ("weekends", "Weekends"),
    ]
    preferred_chat_times = models.JSONField(default=list, blank=True)
    daily_routine_word = models.CharField(max_length=50, blank=True, null=True)

    # Section 2: Interests & Hobbies
    HOBBY_CHOICES = [
        ("gaming", "Gaming"),
        ("reading", "Reading"),
        ("hiking", "Hiking"),
        ("cooking", "Cooking"),
        ("music", "Music"),
        ("art", "Art"),
        ("sports", "Sports"),
        ("other", "Other"),
    ]
    top_hobbies = models.JSONField(default=list, blank=True)
    other_hobbies = models.TextField(blank=True, null=True)

    MEDIA_CHOICES = [
        ("movies_tv", "Movies/TV"),
        ("books_podcasts", "Books/Podcasts"),
        ("music", "Music"),
    ]
    enjoyed_media = models.JSONField(default=list, blank=True)
    media_favorites = models.TextField(blank=True, null=True)
    niche_interests = models.TextField(blank=True, null=True)

    FREE_DAY_CHOICES = [
        ("outdoors_adventure", "Outdoors Adventure"),
        ("cozy_at_home", "Cozy at Home"),
        ("social_gathering", "Social Gathering"),
        ("learning_new", "Learning Something New"),
    ]
    free_day_preference = models.CharField(
        max_length=20, choices=FREE_DAY_CHOICES, blank=True, null=True
    )
    recent_inspiration = models.TextField(blank=True, null=True)
    interested_in_learning = models.BooleanField(default=False)

    # Section 3: Personality & Behaviors
    outgoing_scale = models.IntegerField(blank=True, null=True, help_text="Scale 1-10")

    STRESS_HANDLING_CHOICES = [
        ("talk_it_out", "Talk it out"),
        ("exercise", "Exercise"),
        ("watch_funny_videos", "Watch funny videos"),
        ("meditate", "Meditate"),
        ("other", "Other"),
    ]
    stress_handling = models.CharField(
        max_length=20, choices=STRESS_HANDLING_CHOICES, blank=True, null=True
    )
    stress_handling_other = models.CharField(max_length=100, blank=True, null=True)
    personality_words = models.CharField(max_length=200, blank=True, null=True)

    CONVERSATION_STYLE_CHOICES = [
        ("listener", "Listener"),
        ("talker", "Talker"),
        ("balanced", "Balanced"),
    ]
    conversation_style = models.CharField(
        max_length=10, choices=CONVERSATION_STYLE_CHOICES, blank=True, null=True
    )

    MOTIVATION_CHOICES = [
        ("personal_growth", "Personal Growth"),
        ("fun_adventures", "Fun Adventures"),
        ("helping_others", "Helping Others"),
        ("achieving_goals", "Achieving Goals"),
    ]
    primary_motivation = models.CharField(
        max_length=20, choices=MOTIVATION_CHOICES, blank=True, null=True
    )
    new_things_scale = models.IntegerField(
        blank=True, null=True, help_text="Scale 1-10"
    )

    # Section 4: Values & Communication Style
    FRIENDSHIP_VALUES_CHOICES = [
        ("honesty", "Honesty"),
        ("loyalty", "Loyalty"),
        ("humor", "Humor"),
        ("respect", "Respect"),
        ("empathy", "Empathy"),
    ]
    important_values = models.JSONField(default=list, blank=True)

    COMMUNICATION_STYLE_CHOICES = [
        ("casual_fun", "Casual and Fun"),
        ("deep_thoughtful", "Deep and Thoughtful"),
        ("quick_checkins", "Quick Check-ins"),
        ("structured", "Structured"),
    ]
    communication_preference = models.CharField(
        max_length=20, choices=COMMUNICATION_STYLE_CHOICES, blank=True, null=True
    )

    favorite_topics = models.JSONField(default=list, blank=True)
    topics_to_avoid = models.JSONField(default=list, blank=True)

    CONNECTION_FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("as_needed", "As Needed"),
    ]
    connection_frequency = models.CharField(
        max_length=10, choices=CONNECTION_FREQUENCY_CHOICES, blank=True, null=True
    )

    SERIOUS_CONVERSATION_CHOICES = [
        ("offer_support", "Offer Support"),
        ("lighten_with_humor", "Lighten with Humor"),
        ("change_topic", "Change Topic"),
    ]
    serious_conversation_response = models.CharField(
        max_length=20, choices=SERIOUS_CONVERSATION_CHOICES, blank=True, null=True
    )

    # Section 5: Goals & Preferences
    FRIENDSHIP_GOALS_CHOICES = [
        ("combat_loneliness", "Combat Loneliness"),
        ("gaming_partner", "Gaming Partner"),
        ("motivation_boost", "Motivation Boost"),
        ("cultural_exchange", "Cultural Exchange"),
        ("casual_chats", "Casual Chats"),
    ]
    friendship_goals = models.JSONField(default=list, blank=True)

    FRIEND_PREFERENCES_CHOICES = [
        ("similar_age", "Similar Age"),
        ("shared_culture", "Shared Culture"),
        ("same_gender", "Same Gender"),
        ("focus_on_hobbies", "Focus on Hobbies"),
    ]
    friend_preferences = models.JSONField(default=list, blank=True)
    perfect_friendship_description = models.TextField(blank=True, null=True)

    # Metadata
    completed_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Questionnaire for {self.profile.user.username}"

    def calculate_completion_percentage(self):
        """Calculate completion percentage based on filled fields"""
        required_fields = [
            "age_range",
            "current_location",
            "life_situations",
            "preferred_chat_times",
            "top_hobbies",
            "enjoyed_media",
            "free_day_preference",
            "outgoing_scale",
            "stress_handling",
            "personality_words",
            "conversation_style",
            "primary_motivation",
            "new_things_scale",
            "important_values",
            "communication_preference",
            "favorite_topics",
            "connection_frequency",
            "serious_conversation_response",
            "friendship_goals",
            "friend_preferences",
        ]

        completed_fields = 0
        for field in required_fields:
            value = getattr(self, field)
            if value:
                if isinstance(value, list) and len(value) > 0:
                    completed_fields += 1
                elif not isinstance(value, list) and value is not None:
                    completed_fields += 1

        return (completed_fields / len(required_fields)) * 100


class UserCompatibilityPreferences(BaseModel):
    """
    Model to store user matching preferences and criteria
    """

    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="compatibility_prefs"
    )

    # Matching preferences
    preferred_age_range_min = models.IntegerField(blank=True, null=True)
    preferred_age_range_max = models.IntegerField(blank=True, null=True)

    GENDER_CHOICES = [
        ("any", "Any"),
        ("male", "Male"),
        ("female", "Female"),
        ("non_binary", "Non-binary"),
    ]
    preferred_gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, default="any"
    )
    geographic_preference = models.CharField(max_length=200, blank=True, null=True)

    # Importance weights (1-10 scale)
    hobby_importance = models.IntegerField(default=5)
    personality_importance = models.IntegerField(default=7)
    values_importance = models.IntegerField(default=8)
    lifestyle_importance = models.IntegerField(default=6)

    # Exclusion criteria
    excluded_topics = models.JSONField(default=list, blank=True)
    excluded_personalities = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Compatibility Preferences for {self.profile.user.username}"
