# email api doc
# curl "https://api.postmarkapp.com/email" \
#   -X POST \
#   -H "Accept: application/json" \
#   -H "Content-Type: application/json" \
#   -H "X-Postmark-Server-Token: cbf08161-8ef0-4aab-86ee-c82951780e1a" \
#   -d '{
#         "From": "alphonse@pixelsprint.tech",
#         "To": "alphonse@pixelsprint.tech",
#         "Subject": "Hello from Postmark",
#         "HtmlBody": "<strong>Hello</strong> dear Postmark user.",
#         "MessageStream": "outbound"
#       }'

from django.conf import settings
import requests


class EmailClient:
    def __init__(self):
        self.api_key = settings.POSTMARK_API_KEY
        self.sender_email = settings.POSTMARK_SENDER_EMAIL
        self.api_url = "https://api.postmarkapp.com/email"

    def send_email(self, to: str, subject: str, html_content: str) -> bool:
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
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            # Log the error (omitted for brevity)
            return False
