from core.utils.email_client import EmailClient
from core.utils.logging import LoggingService
import os
from django.conf import settings


class AccountEmails:
    def __init__(self):
        self.email_client = EmailClient()
        self.logger = LoggingService()

    def send_welcome_email(
        self, to_email: str, first_name: str, verification_link
    ) -> bool:
        """
        Send a welcome email to the new user.

        Args:
            to_email (str): Recipient's email address.
            first_name (str): Recipient's first name.
            verification_link (str): Link for email verification.

        Business logic:
            1. Get email template.
            2. Read it a replace placeholders with actual values.
            3. Use EmailClient to send the email.

        Returns:
            bool: True if email sent successfully, False otherwise.

        Error Handling:
            - If sending fails, log the error and return False.
        """
        try:
            subject = "Welcome to Human Link!"
            template_path = os.path.join(
                settings.BASE_DIR, "accounts", "emails_templates", "welcome.html"
            )
            values = {
                "first_name": first_name,
                "verification_link": verification_link,
            }
            html_content = self.process_template(template_path, values)

            # Check if template processing failed
            if html_content is None:
                self.logger.log(
                    f"Failed to process email template for {to_email}", level="error"
                )
                return False

            return self.email_client.send_email(to_email, subject, html_content)
        except Exception as e:
            self.logger.log(
                f"Failed to send welcome email to {to_email}: {str(e)}",
                level="error",
                error=e,
            )
            return False

    def send_password_reset_email(
        self, to_email: str, first_name: str, reset_link: str
    ) -> bool:
        """
        Send a password reset email to the user.

        Args:
            to_email (str): Recipient's email address.
            first_name (str): Recipient's first name.
            reset_link (str): Link for password reset.

        Returns:
            bool: True if email sent successfully, False otherwise.
        """
        try:
            subject = "Reset Your Password - Human Link"
            template_path = os.path.join(
                settings.BASE_DIR,
                "accounts",
                "emails_templates",
                "forget-password.html",
            )
            values = {
                "first_name": first_name,
                "reset_link": reset_link,
            }
            html_content = self.process_template(template_path, values)

            # Check if template processing failed
            if html_content is None:
                self.logger.log(
                    f"Failed to process password reset email template for {to_email}",
                    level="error",
                )
                return False

            return self.email_client.send_email(to_email, subject, html_content)
        except Exception as e:
            self.logger.log(
                f"Failed to send password reset email to {to_email}: {str(e)}",
                level="error",
                error=e,
            )
            return False

    def send_email_verification(
        self, to_email: str, first_name: str, verification_link: str
    ) -> bool:
        """
        Send an email verification link to the user.

        Args:
            to_email (str): Recipient's email address.
            first_name (str): Recipient's first name.
            verification_link (str): Link for email verification.

        Returns:
            bool: True if email sent successfully, False otherwise.
        """
        try:
            subject = "Verify Your Email - Human Link"
            template_path = os.path.join(
                settings.BASE_DIR, "accounts", "emails_templates", "welcome.html"
            )
            values = {
                "first_name": first_name,
                "verification_link": verification_link,
            }
            html_content = self.process_template(template_path, values)

            # Check if template processing failed
            if html_content is None:
                self.logger.log(
                    f"Failed to process email verification template for {to_email}",
                    level="error",
                )
                return False

            return self.email_client.send_email(to_email, subject, html_content)
        except Exception as e:
            self.logger.log(
                f"Failed to send email verification to {to_email}: {str(e)}",
                level="error",
                error=e,
            )
            return False

    def process_template(self, file_path: str, values: dict) -> str:
        """Read an HTML template file and replace placeholders with actual values."""

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                template = file.read()
                for key, value in values.items():
                    # Handle both {{ key }} and {{key}} formats
                    template = template.replace(f"{{{{ {key} }}}}", str(value))
                    template = template.replace(f"{{{{{key}}}}}", str(value))
            return template
        except FileNotFoundError as e:
            self.logger.log(
                f"Email template not found: {file_path} - {str(e)}",
                level="error",
                error=e,
            )
            return None
        except Exception as e:
            self.logger.log(
                f"Error processing email template {file_path}: {str(e)}",
                level="error",
                error=e,
            )
            return None
