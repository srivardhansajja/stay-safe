from django.db import models
from django.urls import reverse
from apps.accounts.models import CustomAccount


class Trip(models.Model):
    trip_owner = models.ForeignKey(CustomAccount,
                        on_delete=models.CASCADE,
                        related_name='trips'
    )
    trip_location = models.CharField(max_length=30)
    trip_name = models.CharField(max_length=30)
    trip_start = models.DateTimeField()
    trip_end = models.DateTimeField()

    def __str__(self):
        return self.trip_name

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)])
