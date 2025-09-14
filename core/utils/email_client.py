from django.conf import settings
import requests


class EmailClient:
    def __init__(self):
        self.api_key = getattr(settings, "POSTMARK_API_KEY", "")
        self.sender_email = getattr(settings, "POSTMARK_SENDER_EMAIL", "")
        self.api_url = "https://api.postmarkapp.com/email"

        # Check if configuration is available
        if not self.api_key or not self.sender_email:
            print(f"⚠️  Email configuration missing:")
            if not self.api_key:
                print("   - POSTMARK_API_KEY not set")
            if not self.sender_email:
                print("   - POSTMARK_SENDER_EMAIL not set")

    def send_email(self, to: str, subject: str, html_content: str) -> bool:
        # Check if we have the required configuration
        if not self.api_key or not self.sender_email:
            print(f"❌ Cannot send email - missing configuration")
            return False

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": self.api_key,
        }
        payload = {
            "From": self.sender_email,
            "To": to,
            "Subject": subject,
            "HtmlBody": html_content,
            "MessageStream": "outbound",
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 422:
                print(f"❌ Postmark API error (422): {response.text}")
                return False
            response.raise_for_status()
            print(f"✅ Email sent successfully to {to}")
            return True
        except requests.RequestException as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
