from django.test import TestCase
from ..models import CustomAccount


class CustomAccountTestCase(TestCase):
    def setUp(self):
        CustomAccount.objects.create(username="bob",
                                     password="123",
                                     email="bob@test.edu",
                                     first_name="bob",
                                     last_name="django")

        CustomAccount.objects.create(username="alice",
                                     password="234",
                                     email="alice@test.edu",
                                     first_name="alice",
                                     last_name="django")

    def test_user_password(self):
        bob = CustomAccount.objects.get(username="bob")
        alice = CustomAccount.objects.get(username="alice")
        self.assertEqual(bob.password, "123")
        self.assertEqual(alice.password, "234")

    def test_user_email(self):
        alice = CustomAccount.objects.get(username="alice")
        self.assertEqual(alice.email, "alice@test.edu")

    def test_user_first_name(self):
        alice = CustomAccount.objects.get(username="alice")
        self.assertEqual(alice.first_name, "alice")

    def test_user_last_name(self):
        alice = CustomAccount.objects.get(username="alice")
        self.assertEqual(alice.last_name, "django")

    def test_retrieve_all(self):
        accounts_list = CustomAccount.objects.all()
        self.assertEqual(len(accounts_list), 2)
