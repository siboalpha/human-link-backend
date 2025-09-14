# Test preferences query service
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile, UserPreferences
from users.tests.factory import ProfileFactory, PreferencesFactory


class TestPreferencesQuery(TestCase):
    """Test class for preferences query operations."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(user=self.user)

    def test_get_preferences_success(self):
        """Test successful retrieval of preferences."""
        preferences = PreferencesFactory(profile=self.profile)

        # Test direct model access
        retrieved_preferences = UserPreferences.objects.get(profile=self.profile)

        self.assertIsNotNone(retrieved_preferences)
        self.assertEqual(retrieved_preferences.id, preferences.id)
        self.assertEqual(retrieved_preferences.age_range, preferences.age_range)

    def test_get_preferences_not_found(self):
        """Test retrieval when preferences do not exist."""
        with self.assertRaises(UserPreferences.DoesNotExist):
            UserPreferences.objects.get(profile=self.profile)

    def test_preferences_choices_validation(self):
        """Test that model choices are valid."""
        preferences_data = {
            "age_range": "25-34",
            "current_location": "New York, USA",
            "life_situations": ["working_professional"],
            "stress_handling": "exercise",
            "conversation_style": "balanced",
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        self.assertEqual(preferences.age_range, "25-34")
        self.assertEqual(preferences.stress_handling, "exercise")
        self.assertEqual(preferences.conversation_style, "balanced")

    def test_calculate_completion_percentage(self):
        """Test completion calculation method."""
        preferences_data = {
            "age_range": "25-34",
            "current_location": "New York, USA",
            "life_situations": ["working_professional"],
            "top_hobbies": ["reading"],
            "outgoing_scale": 7,
            "personality_words": "friendly creative",
            "important_values": ["honesty"],
            "friendship_goals": ["casual_chats"],
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        percentage = preferences.calculate_completion_percentage()
        self.assertGreater(percentage, 0)
        self.assertLessEqual(percentage, 100)
        self.assertIsInstance(percentage, (int, float))

    def test_preferences_validation_edge_cases(self):
        """Test validation with edge cases."""
        # Test with empty lists
        preferences_data = {
            "life_situations": [],
            "top_hobbies": [],
            "important_values": [],
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        self.assertEqual(preferences.life_situations, [])
        self.assertEqual(preferences.top_hobbies, [])
        self.assertEqual(preferences.important_values, [])
