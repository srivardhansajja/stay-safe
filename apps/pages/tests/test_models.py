# apps/pages/tests/test_models.py
import datetime
from django.test import TestCase
from apps.pages.models import Trip, EmergencyContact
from apps.accounts.models import CustomAccount


#
#  Trip Model Unit Tests
#  ---------------------------------------------------------------------------
class TestTripModelFields(TestCase):
    '''
    Test Case:
    Check if Trip objects can be successfully created and retain their
    assigned fields.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Create a user and an associated trip for testing purposes
        '''
        cls.test_user = CustomAccount.objects.create(
            username='TEST_USER_2',
            password='TEST_PASSWORD_2',
            email='TEST_EMAIL_2@EMAIL.COM',
            first_name='TEST_FIRST_NAME',
            last_name='TEST_LAST_NAME'
        )
        Trip.objects.create(
            trip_owner=cls.test_user,
            trip_location='TEST_TRIP_LOCATION',
            trip_name='TEST_TRIP_NAME',
            trip_start='2020-06-15 10:00:00Z',
            trip_end='2020-06-16 10:00:00Z',
        )
        cls.test_trip = Trip.objects.get(trip_owner=cls.test_user)

    @classmethod
    def tearDownClass(cls):
        '''
        Remove the user and associated trip objects from the database
        '''
        cls.test_user.delete()
        cls.test_trip.delete()

    def test_number_of_trips(self):
        '''
        Test: Number of trips created
        '''
        trip_count = len(Trip.objects.all())
        self.assertEqual(trip_count, 1)

    def test_trip_owner(self):
        '''
        Test: The test user owns the test trip
        '''
        self.assertEqual(self.test_user, self.test_trip.trip_owner)

    def test_trip_location(self):
        '''
        Test: Trip location
        '''
        self.assertEqual(self.test_trip.trip_location, 'TEST_TRIP_LOCATION')

    def test_trip_name(self):
        '''
        Test: Trip name
        '''
        self.assertEqual(self.test_trip.trip_name, 'TEST_TRIP_NAME')

    def test_trip_start(self):
        '''
        Test: Trip start date
        '''
        start_date_expected = datetime.datetime.strptime(
            '2020-06-15 10:00:00Z',
            "%Y-%m-%d %H:%M:%S%z"
        )
        self.assertEqual(self.test_trip.trip_start, start_date_expected)

    def test_trip_end(self):
        '''
        Test: Trip end date
        '''
        end_date_expected = datetime.datetime.strptime(
            '2020-06-16 10:00:00Z',
            "%Y-%m-%d %H:%M:%S%z"
        )
        self.assertEqual(self.test_trip.trip_end, end_date_expected)

    def test_trip_str_method(self):
        '''
        Test: Trip __str__ method
        '''
        self.assertEqual(str(self.test_trip), 'TEST_TRIP_NAME')


#
#  EmergencyContact Model Unit Tests
#  ---------------------------------------------------------------------------
class TestEmergencyContactModelFields(TestCase):
    '''
    Test Case:
    Check if EmergencyContact objects can be successfully created and retain
    their assigned fields.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Create an emergency contact associated with a test user
        '''
        cls.test_user = CustomAccount.objects.create(
            username='TEST_USER_2',
            password='TEST_PASSWORD_2',
            email='TEST_EMAIL_2@EMAIL.COM',
            first_name='TEST_FIRST_NAME',
            last_name='TEST_LAST_NAME'
        )
        EmergencyContact.objects.create(
            user=cls.test_user,
            first_name='EMERGENCY_CONTACT_FIRSTNAME',
            last_name='EMERGENCY_CONTACT_LASTNAME',
            email='EMERGENCY_CONTACT@EMAIL.COM',
        )
        cls.test_econtact = EmergencyContact.objects.get(user=cls.test_user)

    @classmethod
    def tearDownClass(cls):
        '''
        Remove the user and associated trip objects from the database
        '''
        cls.test_user.delete()
        cls.test_econtact.delete()

    def test_number_of_emergency_contacts(self):
        '''
        Test: Number of emergency contacts created
        '''
        emergency_contact_count = len(EmergencyContact.objects.all())
        self.assertEqual(emergency_contact_count, 1)

    def test_emergency_contact_owner(self):
        '''
        Test: The test user owns the emergency contact
        '''
        self.assertEqual(self.test_user, self.test_econtact.user)

    def test_emergency_contact_first_name(self):
        '''
        Test: Emergency contact's first name is expected
        '''
        self.assertEqual(
            self.test_econtact.first_name,
            'EMERGENCY_CONTACT_FIRSTNAME'
        )

    def test_emergency_contact_last_name(self):
        '''
        Test: Emergency contact's last name is expected
        '''
        self.assertEqual(
            self.test_econtact.last_name,
            'EMERGENCY_CONTACT_LASTNAME'
        )

    def test_emergency_contact_email(self):
        '''
        Test: Emergency contact's email is expected
        '''
        self.assertEqual(
            self.test_econtact.email,
            'EMERGENCY_CONTACT@EMAIL.COM'
        )
