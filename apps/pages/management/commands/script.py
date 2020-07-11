# pages/management/commands/script.py
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from apps.pages.models import TripStatusList_, Trip, EmergencyContact


class Command(BaseCommand):
    def update_status(self, trip):
        """
        Update the status of the trip object in the database.

            Notes:
                object.save() must be called to save changes to the database.

            Args:
                trip: a trip object

            Returns:
                None
        """
        # Get the current time, trip start date, and trip end dates
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

        # Save changes in the database
        trip.save()

    def send_notificationEmail(self, owner, trip):
        """
        Send an email to the trip owner when a trip is 'Awaiting response'.

            Args:
                owner: a customAccount object
                trip:  a trip object

            Returns:
                None
        """
        # Define email fields
        n = '\n\n'
        sender = 'staysafe3308@gmail.com'
        subject = f'Awaiting response for trip to: {trip.trip_location}!'
        emergency_contact_date = (trip.trip_end + timedelta(hours=1)).strftime(
            '%l:%m%p on %b %d, %Y'
        )

        # Send an email notifying the user that a trip is awaiting response
        message = \
            f'Hello {owner.first_name} {owner.last_name},{n}'\
            f'Your trip to {trip.trip_location} is awaiting your response.{n}'\
            f'If you do not mark this trip as complete, then your emergency '\
            f'contacts will be notified at: {emergency_contact_date} {n}'\
            f'{n}'\
            f'-The Stay Safe Team'
        send_mail(subject, message, sender, [owner.email])

    def send_contactEmails(self, owner, trip):
        """
        Send an email to all of the trip owner's emergency contacts.

            Args:
                owner: a customAccount object
                trip:  a trip object

            Returns:
                None
        """
        # Define email fields
        n = '\n\n'
        name_list = [
            c.first_name for c in EmergencyContact.objects.filter(user=owner)
        ]
        email_list = [
            c.email for c in EmergencyContact.objects.filter(user=owner)
        ]
        end_date = trip.trip_end.strftime('%l:%m%p on %b %d, %Y')
        sender = 'staysafe3308@gmail.com'
        subject = f'{owner.first_name} {owner.last_name}\'s trip ended!'

        # Send an email to each emergency contact
        for contact_name, contact_email in zip(name_list, email_list):
            message = \
                f'Hello {contact_name},{n}'\
                f'{owner.first_name} {owner.last_name}\'s trip to '\
                f'{trip.trip_location} ended 1 hour ago at {end_date}.{n}'\
                f'If you have not heard from them yet, consider contacting'\
                f' them to make sure they are safe.{n}'\
                f'Their email address is: {owner.email}'\
                f'{n}'\
                f'-The Stay Safe Team'
            send_mail(subject, message, sender, [contact_email])

    def handle(self, *args, **kwargs):
        """
        The main logic of this script.

            When run, this script is responsible for executing three methods:
                (1) Update the trip status of all trips.
                (2) Email the user if a trip is "Awaiting response".
                (3) Email emergency contacts if there is no user resopnse.

            Notes:
                The command to run the script is: python manage.py script
                object.save() must be called to save changes to the database.

            Args:
                args:   optional arguments
                kwargs: optional keywoard arguments

            Returns:
                None
        """
        for trip in Trip.objects.all():
            # Ignore trips that have completed and sent a response to contacts
            current_status = trip.trip_status
            if (current_status == "Completed" and trip.response_sent is True):
                continue

            # Update the trip's status
            self.update_status(trip)

            # Send an email to the user if a trip is Awaiting response
            new = trip.trip_status
            if (new == "Awaiting response" and trip.notification is False):
                self.send_notificationEmail(trip.trip_owner, trip)
                trip.notification = True

            # Send an email to contacts if a trip completes with no response
            if (new == "Completed" and trip.response_sent is False):
                self.send_contactEmails(trip.trip_owner, trip)
                trip.response_sent = True

            # Save changes in the database
            trip.save()
        # Shut down the heroku scheduler
        return
