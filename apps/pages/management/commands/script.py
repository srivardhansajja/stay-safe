# pages/management/commands/script.py
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from apps.pages.models import TripStatusList_, Trip, EmergencyContact


class Command(BaseCommand):
    def update_status(self, trip):
        """Update the status of the trip object passed as a parameter.

            Run by 'handle' to update the status of a trip by comparing
            the trip's start and end dates to the date when this script
            executes.

            Args:
                trip: a trip object

            Returns:
                None
        """
        start = trip.trip_start
        end = trip.trip_end
        now = timezone.now()

        # Upcoming
        if (start > now and start <= now + timedelta(days=7)):
            trip.trip_status = TripStatusList_.YTS.value
            print("Upcoming")

        # In progress
        if (start <= now and end > now):
            trip.trip_status = TripStatusList_.IP.value
            print("In progress")

        # Awaiting Response
        if (end < now and end > now - timedelta(hours=1)):
            trip.trip_status = TripStatusList_.AR.value
            print("Awaiting Response")

        # Complete
        if (end < now - timedelta(hours=1)):
            trip.trip_status = TripStatusList_.CP.value
            print("Complete")

    def send_notificationEmail(self, owner, trip):
        pass

    def send_contactEmails(self, owner, trip):
        """Send an email to all of the trip owner's emergency contacts.

            Run by 'handle' when a trip has been Completed but no resposne
            has been sent. This method is not executed if the trip owner
            sets the trip.response_sent field to True during the 1 hour
            grace period after a trip has ended.

            Args:
                owner: a customAccount object
                trip:  a trip object

            Returns:
                None
        """
        name_list = [
            c.first_name for c in EmergencyContact.objects.filter(user=owner)
        ]
        email_list = [
            c.email for c in EmergencyContact.objects.filter(user=owner)
        ]

        # Define email fields
        n = '\n\n'
        end_date = trip.trip_end.strftime('%l:%M%p %Z on %b %d, %Y')
        sender = 'staysafe3308@gmail.com'
        subject = f'{owner.first_name} {owner.last_name}\'s trip ended!'

        # Send an email to each emergency contact
        for name, email in zip(name_list, email_list):
            message = \
                f'Hello {name},{n}'\
                f'{owner.first_name} {owner.last_name}\'s trip to '\
                f'{trip.trip_location} ended 1 hour ago at {end_date}.{n}'\
                f'If you have not heard from them yet, consider contacting'\
                f' them to make sure they are safe.{n}'\
                f'Their email address is: {owner.email}'\
                f'{n}'\
                f'-The Stay Safe Team'
            send_mail(subject, message, sender, [email])

    def handle(self, *args, **kwargs):
        """The main logic of this script.

            When run, this script is responsible for executing three methods:
                (1) Update the trip status of all trips.
                (2) Email the user if a trip is "Awaiting response"
                (3) Email emergency contacts if there is no user resopnse.

            Notes:
                The command to run the script is: $ python manage.py script

            Args:
                args:   optional arguments
                kwargs: optional keywoard arguments

            Returns:
                None
        """
        for trip in Trip.objects.all():
            status = trip.trip_status
            if (status == "Completed" and trip.response_sent is True):
                continue
            self.update_status(trip)
            if (status == "Awaiting response" and trip.notification is False):
                self.send_notificationEmail(trip.trip_owner, trip)
                trip.notification = True
            if (status == "Completed" and trip.response_sent is False):
                self.send_contactEmails(trip.trip_owner, trip)
                trip.response_sent = True
