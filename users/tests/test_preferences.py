# Basic test for user preferences functionality
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserPreferences, UserProfile
from users.tests.factory import ProfileFactory, PreferencesFactory


class PreferencesTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(user=self.user)

    def test_create_preferences(self):
        """Test creating user preferences"""
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
        self.assertEqual(preferences.life_situations, ["working_professional"])
        self.assertEqual(preferences.top_hobbies, ["reading", "gaming"])

    def test_preferences_factory(self):
        """Test preferences factory creates valid objects"""
        preferences = PreferencesFactory()

        self.assertIsInstance(preferences, UserPreferences)
        self.assertIsNotNone(preferences.profile)
        self.assertIsNotNone(preferences.age_range)

    def test_preferences_completion_calculation(self):
        """Test preferences completion percentage calculation"""
        preferences_data = {
            "age_range": "25-34",
            "current_location": "New York, USA",
            "life_situations": ["working_professional"],
            "top_hobbies": ["reading"],
            "outgoing_scale": 7,
            "personality_words": "friendly creative curious",
            "important_values": ["honesty", "humor"],
            "friendship_goals": ["casual_chats"],
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        completion_percentage = preferences.calculate_completion_percentage()
        self.assertGreater(completion_percentage, 0)
        self.assertLessEqual(completion_percentage, 100)

    def test_profile_preferences_relationship(self):
        """Test the relationship between UserProfile and UserPreferences"""
        preferences = PreferencesFactory(profile=self.profile)

        # Test accessing preferences from profile
        self.assertEqual(self.profile.questionnaire, preferences)

        # Test accessing profile from preferences
        self.assertEqual(preferences.profile, self.profile)
