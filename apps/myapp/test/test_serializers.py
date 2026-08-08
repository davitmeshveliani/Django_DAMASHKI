from django.test import TestCase
from django.utils import timezone
import datetime

from apps.myapp.serialisers.home_serializers import TaskCreateSerializer


class SerializerTests(TestCase):

    def setUp(self):
        self.future_deadline = timezone.now() + datetime.timedelta(days=2)
        self.past_deadline = timezone.now() - datetime.timedelta(days=1)

    def test_task_serializer_valid_data(self):
        """ტესტავს Task სერიალიზატორს ვალიდური მონაცემებით"""
        data = {
            "title": "სერიალიზატორის ტესტი",
            "description": "აღწერა",
            "status": "Done",
            "deadline": self.future_deadline
        }
        serializer = TaskCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_task_serializer_past_deadline(self):
        """ტესტავს, რომ სერიალიზატორი ბლოკავს წარსულ დედლაინს"""
        data = {
            "title": "არავალიდური დედლაინი",
            "description": "აღწერა",
            "status": "Done",
            "deadline": self.past_deadline
        }
        serializer = TaskCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("deadline", serializer.errors)