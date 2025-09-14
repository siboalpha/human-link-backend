from django.contrib.auth.models import User, Group
from users.models import UserProfile, UserPreferences, UserCompatibilityPreferences
import factory
from factory.django import DjangoModelFactory
from faker import Faker

fake = Faker()


class UserFactory(DjangoModelFactory):
    """
    Factory for creating User instances for testing.
    Business logic:
        1. Create a User with a unique username and email.
        2. Set a default password for the user.
        3. Optionally assign the user to a group based on the role.

    Usage:
        user = UserFactory(role="User")
    """

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "password123")

    @factory.post_generation
    def role(self, create, extracted, **kwargs):
        """
        Assign a role to the user by adding them to the corresponding group.

        Args:
            create (bool): Whether the instance is being created.
            extracted (str): The role to assign to the user.

        Raises:
            ValueError: If there is an error assigning the role.
        """
        if not create:
            return

        if extracted:
            try:
                group, _ = Group.objects.get_or_create(name=extracted)
                self.groups.add(group)
            except Exception as e:
                raise ValueError(f"Error assigning role '{extracted}': {e}")
        self.save()


class ProfileFactory(DjangoModelFactory):
    """
    Factory for creating UserProfile instances for testing.

    Business logic:
        1. Create a UserProfile linked to a User.
        2. Optionally set the role of the user profile.

    Usage:
        profile = ProfileFactory(role="User")
    """

    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("text", max_nb_chars=200)
    location = factory.Faker("city")
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)
    phone_number = factory.Faker("phone_number")
    avatar = factory.Faker("image_url")
    email_verified = True

    @factory.post_generation
    def role(self, create, extracted, **kwargs):
        """
        Assign a role to the user profile by adding the user to the corresponding group.

        Args:
            create (bool): Whether the instance is being created.
            extracted (str): The role to assign to the user profile.

        Raises:
            ValueError: If there is an error assigning the role.
        """
        if not create:
            return

        if extracted:
            try:
                group, _ = Group.objects.get_or_create(name=extracted)
                self.user.groups.add(group)
            except Exception as e:
                raise ValueError(
                    f"Error assigning role '{extracted}' to user profile: {e}"
                )
        self.user.save()


class PreferencesFactory(DjangoModelFactory):
    """
    Factory for creating UserPreferences instances for testing.

    Business logic:
        1. Create a UserPreferences linked to a UserProfile.
        2. Set realistic test data for all preference fields.
        3. Calculate completion percentage based on filled fields.

    Usage:
        preferences = PreferencesFactory(profile=profile)
    """

    class Meta:
        model = UserPreferences

    profile = factory.SubFactory(ProfileFactory)

    # Demographics
    age_range = factory.Iterator(["18-24", "25-34", "35-44", "45-54", "55+"])
    current_location = factory.Faker("city")

    # Interests
    life_situations = factory.List(["working_professional"])
    preferred_chat_times = factory.List(["evenings"])
    top_hobbies = factory.List(["reading", "gaming"])
    enjoyed_media = factory.List(["movies_tv"])
    free_day_preference = factory.Iterator(
        ["outdoors_adventure", "cozy_at_home", "social_gathering", "learning_new"]
    )

    # Personality
    outgoing_scale = factory.Faker("random_int", min=1, max=10)
    stress_handling = factory.Iterator(
        ["talk_it_out", "exercise", "watch_funny_videos", "meditate", "other"]
    )
    personality_words = factory.Faker("text", max_nb_chars=100)
    conversation_style = factory.Iterator(["listener", "talker", "balanced"])
    primary_motivation = factory.Iterator(
        ["personal_growth", "fun_adventures", "helping_others", "achieving_goals"]
    )
    new_things_scale = factory.Faker("random_int", min=1, max=10)

    # Values
    important_values = factory.List(["honesty", "humor"])
    communication_preference = factory.Iterator(
        ["casual_fun", "deep_thoughtful", "quick_checkins", "structured"]
    )
    favorite_topics = factory.List(["life_advice"])
    connection_frequency = factory.Iterator(["daily", "weekly", "as_needed"])
    serious_conversation_response = factory.Iterator(
        ["offer_support", "lighten_with_humor", "change_topic"]
    )

    # Goals
    friendship_goals = factory.List(["casual_chats"])
    friend_preferences = factory.List(["similar_age"])

    # Completion status
    is_complete = True


class CompatibilityPreferencesFactory(DjangoModelFactory):
    """
    Factory for creating UserCompatibilityPreferences instances for testing.

    Business logic:
        1. Create compatibility preferences linked to a UserProfile.
        2. Set realistic preference weights and criteria.

    Usage:
        preferences = CompatibilityPreferencesFactory(profile=profile)
    """

    class Meta:
        model = UserCompatibilityPreferences

    profile = factory.SubFactory(ProfileFactory)

    preferred_age_range_min = factory.LazyAttribute(
        lambda x: fake.random_int(min=18, max=30)
    )
    preferred_age_range_max = factory.LazyAttribute(
        lambda x: fake.random_int(min=35, max=65)
    )
    preferred_gender = factory.Iterator(["any", "male", "female", "non_binary"])
    geographic_preference = factory.LazyAttribute(lambda x: fake.country())

    hobby_importance = factory.LazyAttribute(lambda x: fake.random_int(min=1, max=10))
    personality_importance = factory.LazyAttribute(
        lambda x: fake.random_int(min=1, max=10)
    )
    values_importance = factory.LazyAttribute(lambda x: fake.random_int(min=1, max=10))
    lifestyle_importance = factory.LazyAttribute(
        lambda x: fake.random_int(min=1, max=10)
    )

    excluded_topics = factory.LazyAttribute(
        lambda x: fake.random_choices(
            elements=["politics", "religion", "work_stress"],
            length=fake.random_int(min=0, max=2),
        )
    )
    excluded_personalities = factory.LazyAttribute(
        lambda x: fake.random_choices(
            elements=["aggressive", "pessimistic", "closed_minded"],
            length=fake.random_int(min=0, max=2),
        )
    )
