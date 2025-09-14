# authentication urls
from django.urls import path
from .views import login_view, signup_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("sign-up/", signup_view, name="sign_up"),
]
