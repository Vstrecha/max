"""
Test script to verify admin panel functionality.
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_panel.settings")
django.setup()

from django.contrib.auth import get_user_model
from stats.models import Profile, Event, EventParticipation, QRScan

User = get_user_model()

print("=" * 50)
print("Admin Panel Test")
print("=" * 50)

# Test 1: Superuser exists
print("\n1. Testing superuser...")
user = User.objects.filter(username="admin").first()
if user:
    print(f"   ✓ Superuser 'admin' exists")
    print(f"   ✓ Is superuser: {user.is_superuser}")
    print(f"   ✓ Is staff: {user.is_staff}")
else:
    print("   ✗ Superuser 'admin' not found")
    sys.exit(1)

# Test 2: Models accessible
print("\n2. Testing models...")
try:
    profiles_count = Profile.objects.count()
    events_count = Event.objects.count()
    participations_count = EventParticipation.objects.count()
    scans_count = QRScan.objects.count()
    print(f"   ✓ Profiles model: {profiles_count} records")
    print(f"   ✓ Events model: {events_count} records")
    print(f"   ✓ Participations model: {participations_count} records")
    print(f"   ✓ QR Scans model: {scans_count} records")
except Exception as e:
    print(f"   ✗ Error accessing models: {e}")
    sys.exit(1)

# Test 3: Database connection
print("\n3. Testing database connection...")
try:
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result:
            print("   ✓ Database connection works")
except Exception as e:
    print(f"   ✗ Database connection error: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("All tests passed! ✓")
print("=" * 50)
