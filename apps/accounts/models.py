# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create custom accounts for the database
class CustomAccount(AbstractUser):
    """TODO: Set custom fields"""
    age = models.PositiveIntegerField(default=0)
