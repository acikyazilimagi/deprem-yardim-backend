from django.core.management.base import BaseCommand, CommandError
from instagram.models import InstagramSession
from instagrapi import Client
from instagrapi.exceptions import BadPassword


class Command(BaseCommand):
    help = "Allows creating an instagram session handling 2FA"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

    def challenge_code_handler(self, username, choice):
        while True:
            code = input(f"Enter code (6 digits) for {username}:").strip()
            if code and code.isdigit():
                return code

    def handle(self, *args, **options):
        client = Client()
        client.challenge_code_handler = self.challenge_code_handler
        try:
            client.login(options["username"], options["password"])
            session = InstagramSession.objects.create(
                settings=client.get_settings(), username=options["username"]
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created session "%s"' % session.pk)
            )
        except BadPassword:
            self.stdout.write("Invalid password")
