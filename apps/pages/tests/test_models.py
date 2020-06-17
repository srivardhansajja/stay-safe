# apps/pages/tests/test_models.py
import datetime
from django.test import TestCase
from apps.pages.models import Trip
from apps.accounts.models import CustomAccount


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
        # User object
        test_user = CustomAccount.objects.create(
            username='TEST_USER_2',
            password='TEST_PASSWORD_2',
            email='TEST_EMAIL_2@EMAIL.COM',
            emergency_email='EMERGENCY_EMAIL_2@EMAIL.COM',
        )

        # Trip object
        Trip.objects.create(
            trip_owner=test_user,
            trip_location='TEST_TRIP_LOCATION',
            trip_name='TEST_TRIP_NAME',
            trip_start='2020-06-15 10:00:00Z',
            trip_end='2020-06-16 10:00:00Z',
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        '''
        Enable the test user and test trip accessible by each test method
        '''
        self.test_user = CustomAccount.objects.get(username='TEST_USER_2')
        self.test_trip = Trip.objects.get(trip_owner=self.test_user)

    def tearDown(self):
        pass

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
        start_date = datetime.datetime.strptime(
            '2020-06-15 10:00:00Z',
            "%Y-%m-%d %H:%M:%S%z"
        )
        self.assertEqual(self.test_trip.trip_start, start_date)

    def test_trip_end(self):
        '''
        Test: Trip end date
        '''
        end_date = datetime.datetime.strptime(
            '2020-06-16 10:00:00Z',
            "%Y-%m-%d %H:%M:%S%z"
        )
        self.assertEqual(self.test_trip.trip_end, end_date)

    def test_trip_str_method(self):
        '''
        Test: Trip __str__ method
        '''
        self.assertEqual(str(self.test_trip), 'TEST_TRIP_NAME')
