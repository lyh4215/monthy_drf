from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
    )
    
    description = models.TextField(
        max_length=100,
        null=True,
    )

    def __str__(self):
        return self.nickname