from django.contrib import admin
from .models import UserProfile, UserPreferences, UserCompatibilityPreferences


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "email_verified", "location", "phone_number", "created_at"]
    list_filter = ["email_verified", "created_at", "updated_at"]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "location",
    ]
    readonly_fields = ["created_at", "updated_at", "email_verification_token"]

    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "user",
                    "bio",
                    "location",
                    "birth_date",
                    "phone_number",
                    "avatar",
                )
            },
        ),
        (
            "Email Verification",
            {
                "fields": (
                    "email_verified",
                    "email_verification_token",
                    "email_verification_sent_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "is_complete",
        "completion_percentage_display",
        "completed_at",
        "created_at",
    ]
    list_filter = ["is_complete", "age_range", "completed_at", "created_at"]
    search_fields = ["profile__user__username", "profile__user__email"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "completed_at",
        "is_complete",
        "completion_percentage_display",
    ]

    def completion_percentage_display(self, obj):
        return f"{obj.calculate_completion_percentage():.1f}%"

    completion_percentage_display.short_description = "Completion %"

    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "profile",
                    "is_complete",
                    "completion_percentage_display",
                    "completed_at",
                )
            },
        ),
        (
            "Demographics & Life Context",
            {
                "fields": (
                    "age_range",
                    "current_location",
                    "life_situations",
                    "preferred_chat_times",
                    "daily_routine_word",
                )
            },
        ),
        (
            "Interests & Hobbies",
            {
                "fields": (
                    "top_hobbies",
                    "other_hobbies",
                    "enjoyed_media",
                    "media_favorites",
                    "niche_interests",
                    "free_day_preference",
                    "recent_inspiration",
                    "interested_in_learning",
                )
            },
        ),
        (
            "Personality & Behaviors",
            {
                "fields": (
                    "outgoing_scale",
                    "stress_handling",
                    "stress_handling_other",
                    "personality_words",
                    "conversation_style",
                    "primary_motivation",
                    "new_things_scale",
                )
            },
        ),
        (
            "Values & Communication",
            {
                "fields": (
                    "important_values",
                    "communication_preference",
                    "favorite_topics",
                    "topics_to_avoid",
                    "connection_frequency",
                    "serious_conversation_response",
                )
            },
        ),
        (
            "Goals & Preferences",
            {
                "fields": (
                    "friendship_goals",
                    "friend_preferences",
                    "perfect_friendship_description",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": ("compatibility_score", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(UserCompatibilityPreferences)
class UserCompatibilityPreferencesAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "preferred_gender",
        "preferred_age_range_display",
        "geographic_preference",
        "created_at",
    ]
    list_filter = ["preferred_gender", "created_at"]
    search_fields = [
        "profile__user__username",
        "profile__user__email",
        "geographic_preference",
    ]
    readonly_fields = ["created_at", "updated_at"]

    def preferred_age_range_display(self, obj):
        if obj.preferred_age_range_min and obj.preferred_age_range_max:
            return f"{obj.preferred_age_range_min}-{obj.preferred_age_range_max}"
        elif obj.preferred_age_range_min:
            return f"{obj.preferred_age_range_min}+"
        elif obj.preferred_age_range_max:
            return f"<{obj.preferred_age_range_max}"
        return "Any"

    preferred_age_range_display.short_description = "Age Range"

    fieldsets = (
        ("Profile", {"fields": ("profile",)}),
        (
            "Basic Preferences",
            {
                "fields": (
                    "preferred_age_range_min",
                    "preferred_age_range_max",
                    "preferred_gender",
                    "geographic_preference",
                )
            },
        ),
        (
            "Importance Weights (1-10)",
            {
                "fields": (
                    "hobby_importance",
                    "personality_importance",
                    "values_importance",
                    "lifestyle_importance",
                )
            },
        ),
        ("Exclusions", {"fields": ("excluded_topics", "excluded_personalities")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
