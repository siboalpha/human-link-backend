# Integration tests for email service - these actually send emails
# Only run these manually or in staging environment
from django.test import TestCase
from accounts.utils.emails import AccountEmails
import os


class TestEmailServiceIntegration(TestCase):
    """
    Integration tests that actually send emails.
    These should only be run manually or in staging environment.

    To run only these tests:
    python manage.py test core.tests.test_email_integration --settings=core.settings_test
    """

    def setUp(self):
        self.email_service = AccountEmails()
        # Only run if we have proper email configuration
        self.skip_if_no_email_config()

    def skip_if_no_email_config(self):
        """Skip tests if email configuration is not available"""
        from django.conf import settings

        if not hasattr(settings, "POSTMARK_API_KEY") or not settings.POSTMARK_API_KEY:
            self.skipTest("Email configuration not available")

    def test_send_welcome_email_integration(self):
        """
        Integration test that actually sends an email.
        Change the email address to your own before running.
        """
        # IMPORTANT: Change this to your email address for testing
        test_email = "your-test-email@example.com"  # Change this!

        if test_email == "your-test-email@example.com":
            self.skipTest("Please set a real email address for integration testing")

        result = self.email_service.send_welcome_email(
            to_email=test_email,
            first_name="TestUser",
            verification_link="http://localhost:8000/verify?token=test123",
        )

        self.assertTrue(result, "Email should be sent successfully")
        print(f"✅ Integration test email sent to {test_email}")
        print("⚠️  Check your inbox to verify the email was received correctly")
