#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django  

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledgebuddy.settings')
    
    django.setup()  # Ensure Django is ready

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowledgebuddy.settings')

    # Import after setting environment variable
    from django.core.management import execute_from_command_line
    from rest_framework_simplejwt.tokens import RefreshToken
    from django.contrib.auth import get_user_model

    # Generate new tokens for the first user (for debugging)
    User = get_user_model()
    user = User.objects.first()  # Select a test user
    if user:
        refresh = RefreshToken.for_user(user)
        print(f"New Refresh Token: {refresh}")
        print(f"New Access Token: {refresh.access_token}")

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
