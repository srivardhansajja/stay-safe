from django.test import TestCase
from ..forms import CustomCreateForm


class CustomCreateFormTest(TestCase):
    def test_form_fields(self):
        form = CustomCreateForm()
        expected = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
