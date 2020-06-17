# apps/pages/tests/test_forms.py
from django.test import TestCase
from apps.pages.forms import TripCreateForm


class TestTripCreateFormFields(TestCase):
    '''
    Test Case:
    Check if the TripCreateForm has the expected fields and data.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Create the test form data
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
        Create an instance of the form for each method and fill it with data
        '''
        self.test_form = TripCreateForm(data=self.test_form_data)

    def tearDown(self):
        pass

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
