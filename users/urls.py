# users urls
from django.urls import path
from .views import (
    preferences_view,
    preferences_status_view,
    preferences_section_update_view,
    preferences_choices_view,
    preferences_sections_view,
    preferences_validate_view,
)

urlpatterns = [
    # User Preferences endpoints
    path("preferences/", preferences_view, name="preferences"),
    path("preferences/status/", preferences_status_view, name="preferences_status"),
    path(
        "preferences/section/<str:section>/",
        preferences_section_update_view,
        name="preferences_section_update",
    ),
    path(
        "preferences/choices/",
        preferences_choices_view,
        name="preferences_choices",
    ),
    path(
        "preferences/sections/",
        preferences_sections_view,
        name="preferences_sections",
    ),
    path(
        "preferences/validate/",
        preferences_validate_view,
        name="preferences_validate",
    ),
]
