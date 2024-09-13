from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from .models import Notifications

class NotificationsModelTest(TestCase):
    def setUp(self):
        # Create a sample notification object to be used in tests
        self.notification = Notifications.objects.create(
            message="Test notification message"
        )

    def test_notification_creation(self):
        """Test if the notification is created successfully"""
        self.assertEqual(self.notification.message, "Test notification message")
        self.assertTrue(self.notification.created_at)  # Checking if created_at is auto-populated

    def test_str_method(self):
        """Test the string representation of the notification"""
        expected_string = f"{self.notification.message},{self.notification.created_at}"
        self.assertEqual(str(self.notification), expected_string)
