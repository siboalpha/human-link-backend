from django.contrib.auth.models import User, Group
from users.models import UserProfile
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

    username = factory.LazyAttribute(lambda x: fake.user_name())
    email = factory.LazyAttribute(lambda x: fake.email())
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
    bio = factory.LazyAttribute(lambda x: fake.text(max_nb_chars=200))
    location = factory.LazyAttribute(lambda x: fake.city())

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
