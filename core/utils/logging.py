# Logging mechanism
import logging
import traceback
from django.conf import settings


class LoggingService:
    """
    A logging service that adapts its behavior based on the environment.
    In development, it logs to the console.
    In production, we will use sentry.io for error tracking and logging.
    """

    def __init__(self):
        self.environment = settings.ENVIRONMENT
        self.sentry_dsn = (
            settings.SENTRY_DSN if hasattr(settings, "SENTRY_DSN") else None
        )

        # Configure Django's logging system
        self.logger = logging.getLogger(__name__)

        # If no handlers are configured, add a console handler for development
        if not self.logger.handlers and self.environment == "development":
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)

        # Initialize Sentry for production
        if self.environment == "production" and self.sentry_dsn:
            import sentry_sdk
            from sentry_sdk.integrations.django import DjangoIntegration
            from sentry_sdk.integrations.logging import LoggingIntegration

            sentry_logging = LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=logging.ERROR,  # Send errors as events
            )

            sentry_sdk.init(
                dsn=self.sentry_dsn,
                integrations=[
                    DjangoIntegration(),
                    sentry_logging,
                ],
                traces_sample_rate=1.0,
                send_default_pii=True,
            )

    def log(self, message: str, level: str = "info", error: Exception = None):
        """Generic logging method that routes to appropriate handlers"""
        level = level.lower()

        if level == "debug":
            self.log_debug(message)
        elif level == "info":
            self.log_info(message)
        elif level == "warning":
            self.log_warning(message)
        elif level == "error":
            self.log_error(message, error)
        elif level == "critical":
            self.log_critical(message, error)
        else:
            self.log_info(message)

    def log_info(self, message: str):
        """Log info level messages"""
        if self.environment == "development":
            self.logger.info(message)
        elif self.environment == "production":
            # In production, use Sentry's breadcrumbs for info messages
            import sentry_sdk

            sentry_sdk.add_breadcrumb(
                message=message,
                level="info",
            )

    def log_error(self, message: str, error: Exception = None):
        """Log error level messages with optional exception details"""
        if self.environment == "development":
            if error:
                self.logger.error(f"{message} - Exception: {str(error)}")
                self.logger.error(f"Traceback: {traceback.format_exc()}")
            else:
                self.logger.error(message)
        elif self.environment == "production":
            # In production, send to Sentry
            import sentry_sdk

            if error:
                sentry_sdk.capture_exception(error)
            else:
                sentry_sdk.capture_message(message, level="error")

    def log_debug(self, message: str):
        """Log debug level messages (only in development)"""
        if self.environment == "development":
            self.logger.debug(message)
        # Debug messages are typically not sent to production logging

    def log_warning(self, message: str):
        """Log warning level messages"""
        if self.environment == "development":
            self.logger.warning(message)
        elif self.environment == "production":
            import sentry_sdk

            sentry_sdk.capture_message(message, level="warning")

    def log_critical(self, message: str, error: Exception = None):
        """Log critical level messages with optional exception details"""
        if self.environment == "development":
            if error:
                self.logger.critical(f"{message} - Exception: {str(error)}")
                self.logger.critical(f"Traceback: {traceback.format_exc()}")
            else:
                self.logger.critical(message)
        elif self.environment == "production":
            # In production, send to Sentry with high priority
            import sentry_sdk

            if error:
                sentry_sdk.capture_exception(error)
            else:
                sentry_sdk.capture_message(message, level="fatal")


# Create a singleton instance for easy import and use
# logger = LoggingService()

# # Usage example (these can be removed in production)
# if __name__ == "__main__":
#     logger.log_info("This is an info message")

#     e = ValueError("An example error")
#     logger.log_error("This is an error message", error=e)
#     logger.log_debug("This is a debug message")
#     logger.log_warning("This is a warning message")
#     logger.log_critical("This is a critical message", error=e)
