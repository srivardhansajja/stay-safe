# apps/pages/tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth import authenticate
from apps.accounts.models import CustomAccount
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
            emergency_email='EMERGENCY_EMAIL@EMAIL.COM',
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
        Test: Successful HTTP request status code
        '''
        self.client.logout()
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_rendered_template_logged_out(self):
        '''
        Test: Intended templates are rendered
        '''
        self.client.logout()
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, '_base.html')

    def test_html_contents_logged_out(self):
        '''
        Test: The view renders the intended html content
        '''
        self.client.logout()
        response = self.client.get('')
        self.assertContains(response, 'You are not logged in', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)

    def test_http_request_status_code_logged_in(self):
        '''
        Test: Successful HTTP request status code
        '''
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_rendered_template_logged_in(self):
        '''
        Test: Intended templates are rendered
        '''
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, '_base.html')

    def test_html_contents_logged_in(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('')
        self.assertContains(response, 'Welcome TEST_USER!', html=True)
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
        self.assertContains(response, 'Scheduled Trips', html=True)
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
        self.assertContains(response, 'Create a Trip', html=True)
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
        response = self.client.get('/trips/add/')
        self.assertContains(response, 'Create a Trip', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)

    def test_password_reset_done_html_contents(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('/trips/add/')
        self.assertContains(response, 'Create a Trip', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)

    def test_password_reset_complete_html_contents(self):
        '''
        Test: Intended html content is rendered
        '''
        response = self.client.get('/trips/add/')
        self.assertContains(response, 'Create a Trip', html=True)
        self.assertNotContains(response, 'test code goes vroooom', html=True)
