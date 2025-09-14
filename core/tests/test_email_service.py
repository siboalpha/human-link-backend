# test email service by testing sending welcome email
from core.tests.setup import BaseTestCase
from accounts.utils.emails import AccountEmails


class TestEmailService(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.email_service = AccountEmails()

    def test_send_welcome_email(self):
        """Test sending a real welcome email through the email service"""
        result = self.email_service.send_welcome_email(
            to_email="sibo.alphonsee@gmail.com",
            first_name="TestUser",
            verification_link="http://localhost:8000/verify?token=test123",
        )
        self.assertTrue(result)
