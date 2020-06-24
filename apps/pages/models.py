from django.db import models
from django.urls import reverse
from apps.accounts.models import CustomAccount
# from apps.accounts.models import TripStatus
from enum import Enum

# Class representing Trip Status, subclass of Enum
class TripStatusList_(Enum):
    YTS = "Yet to start"
    IP = "In progress"
    CP = "Completed"
    ENS = "Emergency notification sent"


class Trip(models.Model):
    trip_owner = models.ForeignKey(CustomAccount,
                                   on_delete=models.CASCADE,
                                   related_name='trips')
    trip_location = models.CharField(max_length=30)
    trip_name = models.CharField(max_length=30)
    trip_start =    models.DateTimeField()
    trip_end = models.DateTimeField()
    trip_status = models.CharField(max_length=5,
                choices=[(tag, tag.value) for tag in TripStatusList_])

    def __str__(self):
        return self.trip_name

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)])


class EmergencyContact(models.Model):
    user = models.ForeignKey(
        CustomAccount,
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        blank=True,
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return f'Contact: {self.first_name} {self.last_name}'
