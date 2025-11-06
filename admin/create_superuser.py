"""
Script to create Django superuser.
Run: python create_superuser.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_panel.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if __name__ == "__main__":
    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists.")
        sys.exit(0)

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
