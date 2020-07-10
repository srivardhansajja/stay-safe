# pages/management/commands/script.py
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from apps.pages.models import TripStatusList_, Trip


class Command(BaseCommand):
    help = 'this is a test lol'

    # method to update a trip's status
    def update_status(self, trip):
        """
        update_status:
            args:
                trip: a trip object
            Description:
                Run by 'handle' to update the status of a trip by comparing
                the trip's start and end dates to the current time.
            returns:
                1: Trip status was updated
                0: Trip status was not updated
        """
        start = trip.trip_start
        end = trip.trip_end
        now = timezone.now()

        # Upcoming
        if (start > now and start <= now + timedelta(days=7)):
            trip.trip_status = TripStatusList_.YTS.value

        # In progress
        if (start <= now and end > now):
            trip.trip_status = TripStatusList_.IP.value

        # Awaiting Response
        if (end < now and end > now - timedelta(hours=1)):
            trip.trip_status = TripStatusList_.AR.value

        # Complete
        if (end < now - timedelta(hours=1)):
            trip.trip_status = TripStatusList_.CP.value

    # method to send an email to an emergency contact
    def send_email(self, contact):
        pass

    # main function of the script
    def handle(self, *args, **kwargs):
        pass
