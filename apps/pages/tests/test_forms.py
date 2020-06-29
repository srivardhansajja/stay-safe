# apps/pages/tests/test_forms.py
from django.test import TestCase
from apps.pages.forms import TripCreateForm, EmergencyContactForm


class TestTripCreateFormFields(TestCase):
    '''
    Test Case:
    Check if the TripCreateForm has the expected fields and data.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Create the test form data and test form instance
        '''
        cls.test_form_data = {
            'trip_location': 'TEST_FORM_LOCATION',
            'trip_name': 'TEST_FORM_TRIP_NAME',
            'trip_start': '2020-06-15T10:00',
            'trip_end': '2020-06-16T10:00',
        }

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        '''
        Create a test form
        '''
        self.test_form = TripCreateForm(data=self.test_form_data)

    def test_form_instance_and_bound(self):
        '''
        Test: Form is a valid, bound instance of TripCreateForm
        '''
        self.assertIsInstance(self.test_form, TripCreateForm)
        self.assertTrue(self.test_form.is_bound)
        self.assertTrue(self.test_form.is_valid())

    def test_form_field_names_and_count(self):
        '''
        Test: Form has four fields and the expected field names
        '''
        form_field_list = list(self.test_form.fields)
        expected_fields = [
            'trip_location',
            'trip_name',
            'trip_start',
            'trip_end'
        ]
        self.assertSequenceEqual(form_field_list, expected_fields)
        self.assertEqual(len(form_field_list), 4)


class TestEmergencyContactFormFields(TestCase):
    '''
    Test Case:
    Check if the EmergencyContactForm has the expected fields and data.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Create the test form data and test form instance
        '''
        cls.test_form_data = {
            'first_name': 'TEST_FIRST_NAME',
            'last_name': 'TEST_LAST_NAME',
            'email': 'TEST@TEST.COM',
        }

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        '''
        Create a test form
        '''
        self.test_form = EmergencyContactForm(data=self.test_form_data)

    def test_form_instance_and_bound(self):
        '''
        Test: Form is a valid, bound instance of TripCreateForm
        '''
        self.assertIsInstance(self.test_form, EmergencyContactForm)
        self.assertTrue(self.test_form.is_bound)
        self.assertTrue(self.test_form.is_valid())

    def test_form_field_names_and_count(self):
        '''
        Test: Form has three fields and the expected field names
        '''
        form_field_list = list(self.test_form.fields)
        expected_fields = [
            'first_name',
            'last_name',
            'email',
        ]
        self.assertSequenceEqual(form_field_list, expected_fields)
        self.assertEqual(len(form_field_list), 3)
