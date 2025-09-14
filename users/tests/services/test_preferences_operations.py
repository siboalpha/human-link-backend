# Test preferences operations service
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile, UserPreferences
from users.tests.factory import ProfileFactory, PreferencesFactory


class TestPreferencesOperations(TestCase):
    """Test class for preferences operations."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(user=self.user)

    def test_create_preferences_success(self):
        """Test successful creation of new preferences."""
        preferences_data = {
            "age_range": "25-34",
            "current_location": "New York, USA",
            "life_situations": ["working_professional"],
            "top_hobbies": ["reading", "gaming"],
            "outgoing_scale": 7,
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        self.assertEqual(preferences.age_range, "25-34")
        self.assertEqual(preferences.current_location, "New York, USA")
        self.assertEqual(preferences.life_situations, ["working_professional"])
        self.assertEqual(preferences.top_hobbies, ["reading", "gaming"])
        self.assertEqual(preferences.outgoing_scale, 7)

    def test_update_preferences_success(self):
        """Test successful update of existing preferences."""
        preferences = PreferencesFactory(profile=self.profile)

        # Update some fields
        preferences.age_range = "35-44"
        preferences.personality_words = "creative ambitious friendly"
        preferences.save()

        updated_preferences = UserPreferences.objects.get(id=preferences.id)
        self.assertEqual(updated_preferences.age_range, "35-44")
        self.assertEqual(
            updated_preferences.personality_words, "creative ambitious friendly"
        )

    def test_delete_preferences_success(self):
        """Test successful deletion of preferences."""
        preferences = PreferencesFactory(profile=self.profile)
        preferences_id = preferences.id

        preferences.delete()

        with self.assertRaises(UserPreferences.DoesNotExist):
            UserPreferences.objects.get(id=preferences_id)

    def test_preferences_completion_calculation(self):
        """Test preferences completion percentage calculation."""
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

        completion_percentage = preferences.calculate_completion_percentage()
        self.assertGreater(completion_percentage, 0)
        self.assertLessEqual(completion_percentage, 100)

    def test_preferences_with_json_fields(self):
        """Test preferences with JSON field data."""
        preferences_data = {
            "life_situations": ["working_professional", "parent"],
            "top_hobbies": ["reading", "gaming", "hiking"],
            "important_values": ["honesty", "humor", "loyalty"],
            "friendship_goals": ["casual_chats", "motivation_boost"],
        }

        preferences = UserPreferences.objects.create(
            profile=self.profile, **preferences_data
        )

        self.assertEqual(len(preferences.life_situations), 2)
        self.assertEqual(len(preferences.top_hobbies), 3)
        self.assertEqual(len(preferences.important_values), 3)
        self.assertEqual(len(preferences.friendship_goals), 2)
