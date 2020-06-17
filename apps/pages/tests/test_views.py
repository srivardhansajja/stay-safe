# apps/pages/tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth import authenticate
from apps.accounts.models import CustomAccount


class TestPageStatusCodes(TestCase):
    '''
    Test Case:
    Check if the status code for each page is 200 which indicates
    a successful HTTP request.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Create a custom account object for testing
        '''
        test_user = CustomAccount.objects.create(
                username='TEST_USER',
                password='TEST_PASSWORD',
                email='TEST_EMAIL@EMAIL.COM',
                emergency_email='EMERGENCY_EMAIL@EMAIL.COM',
                is_active=True,
            )
        test_user.set_password(test_user.password)
        test_user.save()

    @classmethod
    def tearDownClass(cls):
        '''
        Remove the custom account object from the database
        '''
        CustomAccount.objects.all()[0].delete()

    def setUp(self):
        '''
        Login and Authenticate the test user
        '''
        self.client = Client()
        logged_in = self.client.login(
            username='TEST_USER',
            password='TEST_PASSWORD'
        )
        self.assertTrue(logged_in)
        user_auth = authenticate(
            username='TEST_USER',
            password='TEST_PASSWORD',
        )
        self.assertIsNotNone(user_auth)

    def tearDown(self):
        '''
        Logout the test user
        '''
        self.client.logout()

    def test_home_page_status_code(self):
        '''
        Test: Home page access
        '''
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_status_code(self):
        '''
        Test: Login page access
        '''
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        '''
        Test: Signup page access
        '''
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_trips_status_code(self):
        '''
        Test: View Trips page access
        '''
        response = self.client.get('/trips/')
        self.assertEqual(response.status_code, 200)

    def test_create_trips_status_code(self):
        '''
        Test: Add Trips page access
        '''
        response = self.client.get('/trips/add/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_status_code(self):
        '''
        Test: Password Reset page access
        '''
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_status_code(self):
        '''
        Test: Password Reset Done page access
        '''
        response = self.client.get('/accounts/password_reset/done/')
        self.assertEqual(response.status_code, 200)
