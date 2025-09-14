# authentication urls
from django.urls import path
from .views import (
    login_view,
    signup_view,
    verify_email_view,
    resend_verification_email_view,
    password_reset_request_view,
    password_reset_confirm_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("sign-up/", signup_view, name="sign_up"),
    path("verify-email/", verify_email_view, name="verify_email"),
    path(
        "resend-verification/",
        resend_verification_email_view,
        name="resend_verification",
    ),
    path("password-reset/", password_reset_request_view, name="password_reset_request"),
    path(
        "password-reset-confirm/",
        password_reset_confirm_view,
        name="password_reset_confirm",
    ),
]
