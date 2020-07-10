# pages/management/commands/script.py
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'this is a test lol'

    # Methods that can be used by handle
    def hello(self):
        print(self.help)

    # The main function of the script
    def handle(self, *args, **kwargs):
        print(self.help)
        self.hello()
