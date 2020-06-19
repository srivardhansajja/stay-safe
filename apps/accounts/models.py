# apps/accounts/models.py
from django.db.models import EmailField
from django.contrib.auth.models import AbstractUser


# Create custom accounts for the database
class CustomAccount(AbstractUser):
    """Set custom user account fields"""
    emergency_email = EmailField(blank=True, max_length=254)

    email = EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
    )

    def __str__(self):
        return self.username
