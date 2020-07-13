# pages/management/commands/script.py
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from apps.pages.models import TripStatusList_, Trip, EmergencyContact


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        The main logic of this script.

            When run, this script is responsible for executing three methods:
                (1) Update the trip status of all trips.
                (2) Email the user if a trip is "Awaiting response".
                (3) Email emergency contacts if there is no user response.

            The return statement at the end of the for-loop is required. It
            lets the Heroku Scheduler know when it can shut down.
        """
        for trip in Trip.objects.all():
            # Ignore trips that have completed and sent a response to contacts
            current_status = trip.trip_status
            if current_status == "Completed" and trip.response_sent:
                continue

            # Update the trip's status
            trip.update_status()

            # Send an email to the user if a trip is Awaiting response
            new = trip.trip_status
            if new == "Awaiting response" and not trip.notification:
                trip.send_notification_email()
                trip.notification = True

            # Send an email to contacts if a trip completes with no response
            if new == "Completed" and not trip.response_sent:
                trip.send_contact_emails()
                trip.response_sent = True
            trip.save()
        return
