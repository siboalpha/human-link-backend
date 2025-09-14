from django.test import TransactionTestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient


class BaseTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        # Create users directly without using ProfileFactory to avoid circular imports
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.friend = User.objects.create_user(
            username="testfriend", email="friend@example.com", password="testpass123"
        )
        self.user_manager = User.objects.create_user(
            username="usermanager", email="manager@example.com", password="testpass123"
        )
        self.friend_manager = User.objects.create_user(
            username="friendmanager",
            email="fmanager@example.com",
            password="testpass123",
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            is_staff=True,
        )
        self.superuser = User.objects.create_user(
            username="superuser",
            email="super@example.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )

        # Create groups if needed
        user_group, _ = Group.objects.get_or_create(name="User")
        friend_group, _ = Group.objects.get_or_create(name="Friend")
        manager_group, _ = Group.objects.get_or_create(name="User manager")
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        # Assign users to groups
        self.user.groups.add(user_group)
        self.friend.groups.add(friend_group)
        self.user_manager.groups.add(manager_group)
        self.admin.groups.add(admin_group)

        self.client = APIClient()

    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
