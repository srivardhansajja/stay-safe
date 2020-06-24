# apps/accounts/models.py
from django.db.models import EmailField, CharField
from django.contrib.auth.models import AbstractUser


# Create custom accounts for the database
class CustomAccount(AbstractUser):
    """Set custom user account fields"""
    email = EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
            blank=False,
            null=False
    )

    first_name = CharField(
            verbose_name='First name',
            max_length=30,
            blank=False
    )

    last_name = CharField(
            verbose_name='Last name',
            max_length=150,
            blank=False
    )

    def __str__(self):
        return self.username
