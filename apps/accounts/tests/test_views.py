from django.test import TestCase


class SignUpTests(TestCase):
    def test_signup_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)


class LoginTests(TestCase):
    def test_login_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
