# base models
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    deleted_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted_by",
        null=True,
        blank=True,
    )
    archived_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_archived_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
