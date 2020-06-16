from django.test import TestCase
from ..models import CustomAccount


class CustomAccountTestCase(TestCase):
    def setUp(self):
        CustomAccount.objects.create(username="bob",
                                     password="123",
                                     email="bob@test.edu",
                                     emergency_email="alice@test.edu")
        CustomAccount.objects.create(username="alice",
                                     password="234",
                                     email="alice@test.edu",
                                     emergency_email="bob@test.edu")

    def test_user_password(self):
        bob = CustomAccount.objects.get(username="bob")
        alice = CustomAccount.objects.get(username="alice")
        self.assertEqual(bob.password, "123")
        self.assertEqual(alice.password, "234")

    def test_user_email(self):
        alice = CustomAccount.objects.get(username="alice")
        self.assertEqual(alice.email, "alice@test.edu")

    def test_user_emergency_email(self):
        alice = CustomAccount.objects.get(username="alice")
        self.assertEqual(alice.emergency_email, "bob@test.edu")

    def test_retrieve_all(self):
        accounts_list = CustomAccount.objects.all()
        self.assertEqual(len(accounts_list), 2)
