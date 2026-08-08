from django.test import TestCase
from django.utils import timezone
import datetime
from rest_framework.test import APITestCase

from apps.myapp.models import Category, Task, SubTask
from apps.myapp.serialisers.home_serializers import TaskCreateSerializer


class ComprehensiveProjectTests(APITestCase):

    def setUp(self):
        # ვქმნით დამხმარე კატეგორიას ტესტებისთვის
        self.category = Category.objects.create(name="პროგრამირება")
        self.future_deadline = timezone.now() + datetime.timedelta(days=5)
        self.past_deadline = timezone.now() - datetime.timedelta(days=2)

    def test_category_creation(self):
        """ამოწმებს კატეგორიის სწორად შექმნას"""
        self.assertEqual(self.category.name, "პროგრამირება")
        self.assertEqual(str(self.category), "პროგრამირება")

    def test_task_model_with_categories(self):
        """ამოწმებს Task მოდელისა და ManyToMany კავშირის შექმნას"""
        task = Task.objects.create(
            title="ტესტური დავალება",
            description="აღწერა",
            status="In progress",
            deadline=self.future_deadline
        )
        # ვამატებთ კატეგორიას ManyToMany ველში
        task.categories.add(self.category)

        self.assertEqual(task.title, "ტესტური დავალება")
        self.assertIn(self.category, task.categories.all())

    def test_serializer_with_valid_data(self):
        """ამოწმებს სერიალიზატორს სწორი მონაცემებით და In progress სტატუსით"""
        data = {
            "title": "Django ტესტი",
            "description": "დეტალური ტესტირება",
            "status": "In progress",
            "deadline": self.future_deadline
        }
        serializer = TaskCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_rejects_past_deadline(self):
        """ამოწმებს, რომ სერიალიზატორი ბლოკავს წარსულ დედლაინს"""
        data = {
            "title": "ძველი დავალება",
            "description": "ტესტი",
            "status": "Done",
            "deadline": self.past_deadline
        }
        serializer = TaskCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("deadline", serializer.errors)

    def test_subtask_creation(self):
        """ამოწმებს SubTask მოდელის შექმნას და მთავარ Task-თან კავშირს"""
        task = Task.objects.create(
            title="მთავარი დავალება",
            status="New"
        )
        subtask = SubTask.objects.create(
            title="ქვედავალება 1",
            task=task,
            status="New"
        )
        self.assertEqual(subtask.task, task)
        self.assertEqual(subtask.title, "ქვედავალება 1")
        self.assertIn(subtask, task.subtasks.all())