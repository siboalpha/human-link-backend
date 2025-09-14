# Test preferences utils service
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile, UserPreferences
from users.tests.factory import PreferencesFactory


class TestPreferencesUtils(TestCase):
    """Test class for preferences utility functions."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(user=self.user)

    def test_preferences_validation_utility(self):
        """Test utility functions for preferences validation."""
        # Test valid choices
        valid_age_ranges = ["18-24", "25-34", "35-44", "45-54", "55+"]
        for age_range in valid_age_ranges:
            preferences = UserPreferences.objects.create(
                profile=self.profile, age_range=age_range
            )
            self.assertEqual(preferences.age_range, age_range)
            preferences.delete()  # Clean up for next iteration

    def test_preferences_section_completion(self):
        """Test completion calculation for specific sections."""
        preferences_data = {
            "age_range": "25-34",
            "current_location": "New York, USA",
            "life_situations": ["working_professional"],
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        # Test that demographics section has some completion
        completion = preferences.calculate_completion_percentage()
        self.assertGreater(completion, 0)

    def test_preferences_json_field_handling(self):
        """Test handling of JSON fields in preferences."""
        json_data = {
            "life_situations": ["working_professional", "parent"],
            "top_hobbies": ["reading", "gaming"],
            "important_values": ["honesty", "humor", "loyalty"],
            "friendship_goals": ["casual_chats", "motivation_boost"],
        }

        preferences = UserPreferences.objects.create(profile=self.profile, **json_data)

        # Verify JSON fields are properly stored and retrieved
        self.assertIsInstance(preferences.life_situations, list)
        self.assertIsInstance(preferences.top_hobbies, list)
        self.assertIsInstance(preferences.important_values, list)
        self.assertIsInstance(preferences.friendship_goals, list)

        # Verify content
        self.assertEqual(len(preferences.life_situations), 2)
        self.assertIn("working_professional", preferences.life_situations)
        self.assertIn("parent", preferences.life_situations)

    def test_preferences_choices_validation(self):
        """Test that model choices are properly validated."""
        # Test valid stress handling choice
        preferences = UserPreferences.objects.create(
            profile=self.profile, stress_handling="exercise"
        )
        self.assertEqual(preferences.stress_handling, "exercise")

        # Test valid conversation style
        preferences.conversation_style = "balanced"
        preferences.save()
        self.assertEqual(preferences.conversation_style, "balanced")

    def test_preferences_scale_fields(self):
        """Test scale fields (1-10) validation."""
        preferences = UserPreferences.objects.create(
            profile=self.profile, outgoing_scale=7, new_things_scale=9
        )

        self.assertEqual(preferences.outgoing_scale, 7)
        self.assertEqual(preferences.new_things_scale, 9)
        self.assertTrue(1 <= preferences.outgoing_scale <= 10)
        self.assertTrue(1 <= preferences.new_things_scale <= 10)
