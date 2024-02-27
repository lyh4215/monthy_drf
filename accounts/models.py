from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    address = models.CharField(
        max_length=15,
        unique=True,
        null=True,
    )
    
    description = models.TextField(
        max_length=100,
        blank=True,
        null=True,
    )

    profile_image = models.ImageField(
        upload_to='profile_image',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username or "username is None"