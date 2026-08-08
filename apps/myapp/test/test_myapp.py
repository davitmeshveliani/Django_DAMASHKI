from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.myapp.models import Category, Task, SubTask
from django.utils import timezone
import datetime


class MyAppApiTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="ტექნოლოგიები")
        self.future_deadline = timezone.now() + datetime.timedelta(days=2)
        self.past_deadline = timezone.now() - datetime.timedelta(days=1)

    def test_get_tasks_list(self):
        """ტესტავს დავალებების სიის წამოღებას"""
        Task.objects.create(
            title="ტესტური დავალება",
            description="აღწერა",
            status="Done",
            deadline=self.future_deadline
        )
        url = '/api/myapp/tasks/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_task_deadline_validation_via_api(self):
        """ტესტავს, რომ წარსული დედლაინით დავალება არ იქმნება (API დონეზე)"""
        url = '/api/myapp/tasks/'
        data = {
            "title": "წარსული დედლაინი",
            "description": "ტესტი",
            "status": "Done",
            "deadline": self.past_deadline.isoformat()
        }

        response = self.client.post(url, data, format='json')
        # უნდა დააბრუნოს 400 Bad Request რადგან დედლაინი წარსულშია
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)