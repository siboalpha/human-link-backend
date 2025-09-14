from django.test import TransactionTestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient

from users.tests.factory import ProfileFactory


class BaseTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):

        self.user = ProfileFactory(role="User")
        self.friend = ProfileFactory(role="Friend")
        self.user_manager = ProfileFactory(role="User manager")
        self.friend_manager = ProfileFactory(role="Friend manager")
        self.admin = ProfileFactory(role="Admin")
        self.superuser = ProfileFactory(role="Superuser")
        self.client = APIClient()

    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
