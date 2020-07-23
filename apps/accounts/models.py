# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

# Create custom accounts for the database
class CustomAccount(AbstractUser):
    """Set custom user account fields"""
    email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
            blank=False,
            null=False
    )

    first_name = models.CharField(
            verbose_name='First name',
            max_length=30,
            blank=False
    )

    last_name = models.CharField(
            verbose_name='Last name',
            max_length=150,
            blank=False
    )

    eButton_date = models.DateTimeField(
        default=(timezone.now() - timedelta(minutes=3))
    )

    def __str__(self):
        return self.username
