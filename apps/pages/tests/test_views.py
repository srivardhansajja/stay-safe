# apps/pages/tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth import authenticate
from apps.accounts.models import CustomAccount
from django.contrib.messages import get_messages
from django.contrib import auth


#
#  User Login Unit Tests
#  ---------------------------------------------------------------------------
class TestUserLogin(TestCase):
    '''
    Test Case: User login and authentication
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Create a test user for accessing authenticated paths
        '''
        cls.test_user = CustomAccount.objects.create(
            username='TEST_USER',
            password='TEST_PASSWORD',
            email='TEST_EMAIL@EMAIL.COM',
            first_name='TEST_FIRST_NAME',
            last_name='TEST_LAST_NAME',
            is_active=True,
        )
        cls.test_user.set_password(cls.test_user.password)
        cls.test_user.save()

    @classmethod
    def tearDownClass(cls):
        '''
        Remove the test user from the database
        '''
        cls.test_user.delete()

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

    def test_authentication(self):
        '''
        Test: Login will authenticate the test user
        '''
        # Check if a logged-in user is authenticated
        test_user_auth = auth.get_user(self.client)
        self.assertTrue(test_user_auth.is_authenticated)

        # Check if a logged-out user is not authenticated
        self.client.logout()
        test_user_auth = auth.get_user(self.client)
        self.assertFalse(test_user_auth.is_authenticated)


#
#  HomePageView Unit Tests
#  ---------------------------------------------------------------------------
class TestHomePageView(TestUserLogin):
    '''
    Test Case: HomePageView in apps/pages/views.py
    '''
    def test_http_request_status_code_logged_out(self):
        '''
        Test: Logged out users accessing the homepage URL are presented
              with the intended content from the home and base templates.
        '''
        self.client.logout()
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, '_base.html')
        self.assertContains(response, 'Welcome to Stay Safe!', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)

    def test_http_request_status_code_logged_in(self):
        '''
        Test: Logged in users accessing the homepage URL are presented
              with the intended content from the home and base templates.
        '''
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, '_base.html')
        self.assertContains(response, 'Welcome, TEST_FIRST_NAME!', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)


#
#  TripPageView Unit Tests
#  ---------------------------------------------------------------------------
class TestTripPageView(TestUserLogin):
    '''
    Test Case: TripPageView in apps/pages/views.py
    '''
    def test_logout_redirect(self):
        '''
        Test: Logged-out users attempting to access restricted URLs are
              redirected to the login page.
        '''
        self.client.logout()
        response = self.client.get('/trips/')
        self.assertRedirects(response, '/accounts/login/?next=/trips/')

    def test_http_request_status_code(self):
        '''
        Test: Successful HTTP request status code
        '''
        response = self.client.get('/trips/')
        self.assertEqual(response.status_code, 200)

    def test_rendered_template(self):
        '''
        Test: Intended templates are rendered
        '''
        response = self.client.get('/trips/')
        self.assertTemplateUsed(response, 'trip_view.html')
        self.assertTemplateUsed(response, '_base.html')

    def test_html_contents(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('/trips/')
        self.assertContains(response, 'Scheduled trips', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)


#
#  TripCreateView Unit Tests
#  ---------------------------------------------------------------------------
class TestTripCreateView(TestUserLogin):
    '''
    Test Case: TripCreateView in apps/pages/views.py
    '''
    def test_logout_redirect(self):
        '''
        Test: Logged-out users attempting to access restricted URLs are
              redirected to the login page.
        '''
        self.client.logout()
        response = self.client.get('/trips/add/')
        self.assertRedirects(response, '/accounts/login/?next=/trips/add/')

    def test_http_request_status_code(self):
        '''
        Test: Successful HTTP request status code
        '''
        response = self.client.get('/trips/add/')
        self.assertEqual(response.status_code, 200)

    def test_rendered_template(self):
        '''
        Test: Intended templates are rendered
        '''
        response = self.client.get('/trips/add/')
        self.assertTemplateUsed(response, 'trip_create.html')
        self.assertTemplateUsed(response, '_base.html')

    def test_html_contents(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('/trips/add/')
        self.assertContains(response, 'Create a new trip', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)


#
#  Password Reset Unit Tests
#  ---------------------------------------------------------------------------
class TestPasswordResetView(TestUserLogin):
    '''
    Test Case: PasswordReset views in apps/pages/views.py
    '''
    def test_password_reset_status_code(self):
        '''
        Test: Successful HTTP request status code
        '''
        response1 = self.client.get('/password_reset/')
        response2 = self.client.get('/accounts/password_reset/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_password_reset_done_status_code(self):
        '''
        Test: Successful HTTP request status code
        '''
        response1 = self.client.get('/password_reset/done/')
        response2 = self.client.get('/accounts/password_reset/done/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_password_reset_complete_status_code(self):
        '''
        Test: Successful HTTP request status code
        '''
        response1 = self.client.get('/reset/done/')
        response2 = self.client.get('/accounts/reset/done/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_password_reset_rendered_template(self):
        '''
        Test: Intended templates are rendered
        '''
        response = self.client.get('/password_reset/')
        self.assertTemplateUsed(
            response,
            'registration/password_reset_form.html'
        )
        self.assertTemplateUsed(response, '_base.html')

    def test_password_reset_done_rendered_template(self):
        '''
        Test: Intended templates are rendered
        '''
        response = self.client.get('/password_reset/done/')
        self.assertTemplateUsed(
            response,
            'registration/password_reset_done.html'
        )
        self.assertTemplateUsed(response, '_base.html')

    def test_password_reset_complete_rendered_template(self):
        '''
        Test: Intended templates are rendered
        '''
        response = self.client.get('/reset/done/')
        self.assertTemplateUsed(
            response,
            'registration/password_reset_complete.html'
        )
        self.assertTemplateUsed(response, '_base.html')

    def test_password_reset_html_contents(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('/password_reset/')
        self.assertContains(response, 'Password Reset', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)

    def test_password_reset_done_html_contents(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('/password_reset/done/')
        self.assertContains(response, 'Reset email sent!', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)

    def test_password_reset_complete_html_contents(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('/reset/done/')
        self.assertContains(response, 'Password reset complete', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)


#
#  Add Emergency Contact Unit Tests
#  ---------------------------------------------------------------------------
class TestEmergencyContactCreateView(TestUserLogin):
    '''
    Test Case: EmergencyContactCreateView in apps/pages/views.py
    '''
    def test_logout_redirect(self):
        '''
        Test: Logged-out users attempting to access restricted URLs are
              redirected to the login page.
        '''
        self.client.logout()
        response = self.client.get('/emergencycontacts/')
        self.assertRedirects(
            response, '/accounts/login/?next=/emergencycontacts/'
        )

    def test_http_request_status_code(self):
        '''
        Test: Logged in users accessing the homepage URL are presented
              with the intended content from the emergency contact templates.
        '''
        response = self.client.get('/emergencycontacts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emergencycontact_view.html')
        self.assertTemplateUsed(response, '_base.html')
        self.assertContains(response, 'Emergency Contacts', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)

    def test_max_emergency_contact_redirect(self):
        '''
        Test: Adding more than 5 emergency contacts is not allowed
        '''
        CONTACTS_EMAILS = [
            'ONE__@EMAIL.COM',
            'TWO__@EMAIL.COM',
            'THREE@EMAIL.COM',
            'FOUR_@EMAIL.COM',
            'FIVE_@EMAIL.COM',
        ]

        # Create 5 emergency contacts by posting to the form
        for addr in CONTACTS_EMAILS:
            response = self.client.post(
                '/emergencycontact/add/',
                {
                    'first_name': addr[0:5],
                    'last_name': addr[0:1],
                    'email': addr
                }
            )

        # Check if there are 5 emergency contacts
        self.assertEqual(len(self.test_user.emergency_contacts.all()), 5)

        # Add a sixth emergency contact
        response = self.client.post(
            '/emergencycontact/add/',
            {
                'first_name': 'SIX',
                'last_name': 'SIX',
                'email': 'SIX@EMAIL.COM'
            }
        )

        # Check for an error message
        message_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(message_list), 1)
        self.assertEqual(
            str(message_list[0]),
            'max'
        )

        # Check if there are still 5 emergency contacts
        self.assertEqual(len(self.test_user.emergency_contacts.all()), 5)

        # Check whether a redirect to the form occurred
        self.assertEqual(response.status_code, 302)

    def test_max_emergency_contact_unique(self):
        '''
        Test: Adding the same emergency contact email is not allowed
        '''
        CONTACTS_EMAILS = [
            'ONE__@EMAIL.COM',
            'ONE__@EMAIL.COM',
        ]

        # Add two emergency contacts with the same email
        for addr in CONTACTS_EMAILS:
            response = self.client.post(
                '/emergencycontact/add/',
                {
                    'first_name': addr[0:5],
                    'last_name': addr[0:1],
                    'email': addr
                }
            )

        # Check that there is only one emergency contact (second not added)
        self.assertEqual(len(self.test_user.emergency_contacts.all()), 1)

        # Check for an error message (labeled 'dup' in pages/views.py)
        message_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(message_list), 1)
        self.assertEqual(
            str(message_list[0]),
            'dup'
        )

        # Check whether a redirect to the form occurred
        self.assertEqual(response.status_code, 302)

        # Check whether another user can add the same emergency contact
        test_user_2 = CustomAccount.objects.create(
            username='TEST_USER_TWO',
            password='TEST_PASSWORD',
            email='TEST_EMAIL_TWO@EMAIL.COM',
            first_name='TEST_FIRST_NAME',
            last_name='TEST_LAST_NAME',
            is_active=True,
        )
        # Login the second test user
        test_user_2.set_password(test_user_2.password)
        test_user_2.save()
        client_2 = Client()
        client_2.login(username='TEST_USER_TWO', password='TEST_PASSWORD')
        authenticate(username='TEST_USER_TWO', password='TEST_PASSWORD')

        # Assign the second test user the same emergency contact as the first
        for addr in CONTACTS_EMAILS:
            response = client_2.post(
                '/emergencycontact/add/',
                {
                    'first_name': addr[0:5],
                    'last_name': addr[0:1],
                    'email': addr
                }
            )

        # Check that there is one emergency contact added for the second user
        self.assertEqual(len(self.test_user.emergency_contacts.all()), 1)

        # Check that the emergency contact for both test users is the same
        self.assertEqual(
            self.test_user.emergency_contacts.values('email')[0],
            test_user_2.emergency_contacts.values('email')[0]
        )

        # Logout the second test user
        client_2.logout()
        test_user_2.delete()
