# Generate verification token
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class TokenGenerator:

    @staticmethod
    def generate_verification_token(
        user_id: int, token_type: str = "email_verification"
    ) -> str:
        """Generate a JWT token for email verification or password reset."""
        # Set different expiration times based on token type
        if token_type == "password_reset":
            expiration_hours = 1  # Password reset tokens expire in 1 hour for security
        else:
            expiration_hours = 24  # Email verification tokens expire in 24 hours

        payload = {
            "user_id": user_id,
            "token_type": token_type,
            "exp": datetime.utcnow() + timedelta(hours=expiration_hours),
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def decode_verification_token(token: str) -> dict:
        """Decode the JWT token and return the payload."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}

    @staticmethod
    def generate_email_verification_token(user_id: int) -> str:
        """Generate a token specifically for email verification."""
        return TokenGenerator.generate_verification_token(user_id, "email_verification")

    @staticmethod
    def generate_password_reset_token(user_id: int) -> str:
        """Generate a token specifically for password reset."""
        return TokenGenerator.generate_verification_token(user_id, "password_reset")

    @staticmethod
    def verify_token(token: str, expected_type: str) -> dict:
        """Verify a token and check if it matches the expected type."""
        payload = TokenGenerator.decode_verification_token(token)

        if "error" in payload:
            return payload

        if payload.get("token_type") != expected_type:
            return {"error": "Invalid token type"}

        return payload
