import django
django.setup()  # Ensure Django is initialized before importing models

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class Command(BaseCommand):
    help = "Generate a JWT token for the first user"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("No users found in the database!"))
            return

        refresh = RefreshToken.for_user(user)
        self.stdout.write(self.style.SUCCESS(f"New Refresh Token: {refresh}"))
        self.stdout.write(self.style.SUCCESS(f"New Access Token: {refresh.access_token}"))
