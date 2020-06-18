# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


# Create custom accounts for the database
class CustomAccount(AbstractUser):
    """Set custom user account fields"""
    emergency_email = models.EmailField(blank=True, max_length=254)

    email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
    )

    def __str__(self):
        return self.username

# Class representing Trip Status, subclass of Enum
class TripStatus(Enum):
    YTS = "Yet to start"
    IP = "In progress"
    CP = "Completed"
    ENS = "Emergency notification sent"
