from django.core.management import BaseCommand
from django.contrib.auth.models import User
import environ


class Command(BaseCommand):
    def handle(self, *args, **options):
        env = environ.Env()
        default_password = env("DEFAULT_ADMIN_PASSWORD")
        default_username = "depremyardim"
        if not User.objects.filter(username=default_username).exists():
            user = User.objects.create(username=default_username, is_active=True, is_staff=True, is_superuser=True)
            user.set_password(default_password)
            user.save()
