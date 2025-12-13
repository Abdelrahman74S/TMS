from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Profile(AbstractUser):
    profile_uuid=models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}'s profile"