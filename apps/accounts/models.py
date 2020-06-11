# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create custom accounts for the database
class CustomAccount(AbstractUser):
    """Set custom user account fields"""
    emergency_email = models.EmailField(blank=True, max_length=254)

    def __str__(self):
        return self.username
