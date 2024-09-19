from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileTest(TestCase):
    def test_profile_creation(self):
        user = User.objects.create(username="testuser", password="password123")
        self.assertIsInstance(user.profile, Profile)  # Check that profile is automatically created

    def test_profile_data(self):
        user = User.objects.create(username="testuser", password="password123")
        profile = user.profile
        profile.nic_passport_no = "123456789V"
        profile.mobile_no = "+1234567890"
        profile.save()
        self.assertEqual(profile.nic_passport_no, "123456789V")
        self.assertEqual(profile.mobile_no, "+1234567890")

