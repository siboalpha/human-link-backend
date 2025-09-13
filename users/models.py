from django.db import models

from core.models import BaseModel


# Create your models here.
class UserProfile(BaseModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name if self.user.first_name else ""} {self.user.last_name if self.user.last_name else self.user.username}"
