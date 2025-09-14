# Test preferences endpoints
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from users.models import UserProfile, UserPreferences
from users.tests.factory import PreferencesFactory


class TestPreferencesEndpoint(TestCase):
    """Test class for preferences endpoint basic functionality."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_preferences_model_creation(self):
        """Test that preferences can be created successfully."""
        preferences_data = {
            "age_range": "25-34",
            "current_location": "New York, USA",
            "life_situations": ["working_professional"],
            "top_hobbies": ["reading", "gaming"],
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        self.assertEqual(preferences.age_range, "25-34")
        self.assertEqual(preferences.current_location, "New York, USA")

    def test_preferences_factory_integration(self):
        """Test that preferences factory works correctly."""
        preferences = PreferencesFactory(profile=self.profile)

        self.assertIsInstance(preferences, UserPreferences)
        self.assertEqual(preferences.profile, self.profile)
        self.assertIsNotNone(preferences.age_range)

    def test_user_profile_preferences_relationship(self):
        """Test the relationship between UserProfile and UserPreferences."""
        preferences = PreferencesFactory(profile=self.profile)

        # Test one-to-one relationship
        self.assertEqual(self.profile.questionnaire, preferences)
        self.assertEqual(preferences.profile, self.profile)

    def test_preferences_completion_calculation(self):
        """Test preferences completion percentage calculation."""
        preferences_data = {
            "age_range": "25-34",
            "current_location": "New York, USA",
            "life_situations": ["working_professional"],
            "top_hobbies": ["reading"],
            "outgoing_scale": 7,
            "personality_words": "friendly creative",
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        completion = preferences.calculate_completion_percentage()
        self.assertGreater(completion, 0)
        self.assertLessEqual(completion, 100)

    def test_preferences_str_method(self):
        """Test string representation of preferences."""
        preferences = PreferencesFactory(profile=self.profile)

        expected_str = f"Questionnaire for {self.user.username}"
        self.assertEqual(str(preferences), expected_str)
