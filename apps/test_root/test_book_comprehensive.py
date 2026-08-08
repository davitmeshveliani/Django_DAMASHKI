from django.utils import timezone
import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.book.models import BookAuthor, BookCategory, Book, BookTask, BookSubTask, CommonStatus
from apps.book.serialisers.book_serializers import BookTaskCreateSerializer


class BookComprehensiveTests(APITestCase):

    def setUp(self):
        self.author = BookAuthor.objects.create(
            name="ოთარ ჭილაძე",
            bio="ქართველი მწერალი და პოეტი"
        )
        self.category = BookCategory.objects.create(
            name="რომანი"
        )
        self.future_date = timezone.now().date() + datetime.timedelta(days=10)
        self.future_deadline = timezone.now() + datetime.timedelta(days=7)
        self.past_deadline = timezone.now() - datetime.timedelta(days=2)

        self.book = Book.objects.create(
            title="ყოველმან პატიოსანმან",
            author=self.author,
            category=self.category,
            published_date=self.future_date,
            status=CommonStatus.PUBLISHED
        )
        self.authors_url = reverse('book-author-list-create')
        self.books_url = reverse('book-list-create')

    def test_book_author_creation(self):
        """ამოწმებს BookAuthor მოდელის შექმნასა და __str__ მეთოდს"""
        self.assertEqual(self.author.name, "ოთარ ჭილაძე")
        self.assertEqual(str(self.author), "ოთარ ჭილაძე")

    def test_book_category_creation(self):
        """ამოწმებს BookCategory მოდელის შექმნას"""
        self.assertEqual(self.category.name, "რომანი")
        self.assertEqual(str(self.category), "რომანი")

    def test_book_creation_with_relations(self):
        """ამოწმებს Book მოდელის შექმნას ავტორთან, კატეგორიასთან და სტატუსთან ერთად"""
        self.assertEqual(self.book.title, "ყოველმან პატიოსანმან")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.category, self.category)
        self.assertEqual(self.book.status, CommonStatus.PUBLISHED)
        self.assertEqual(str(self.book), "ყოველმან პატიოსანმან")

    def test_book_task_and_subtask_creation(self):
        """ამოწმებს BookTask და BookSubTask მოდელების ურთიერთკავშირს"""
        task = BookTask.objects.create(
            title="წიგნის რედაქტირება",
            category=self.category,
            description="თავების გადამოწმება",
            status=CommonStatus.IN_PROGRESS
        )
        subtask = BookSubTask.objects.create(
            task=task,
            title="პირველი თავის გასწორება",
            status=CommonStatus.NEW
        )

        self.assertEqual(task.title, "წიგნის რედაქტირება")
        self.assertEqual(subtask.task, task)
        self.assertIn(subtask, task.book_subtasks.all())
        self.assertEqual(str(task), "წიგნის რედაქტირება")
        self.assertEqual(str(subtask), "პირველი თავის გასწორება")

    def test_book_task_serializer_valid_data(self):
        """ამოწმებს BookTask სერიალიზატორს სწორი მონაცემებით"""
        data = {
            "title": "გარეკანის დიზაინი",
            "category": self.category.id,
            "description": "ახალი პროექტი",
            "status": CommonStatus.IN_PROGRESS,
            "deadline": self.future_deadline
        }
        serializer = BookTaskCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_book_task_serializer_rejects_past_deadline(self):
        """ამოწმებს, რომ BookTask სერიალიზატორი ბლოკავს წარსულ დედლაინს"""
        data = {
            "title": "ძველი დავალება",
            "category": self.category.id,
            "status": CommonStatus.NEW,
            "deadline": self.past_deadline
        }
        serializer = BookTaskCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("deadline", serializer.errors)

    def test_get_authors_api(self):
        """ამოწმებს ავტორების API-ს (GET)"""
        response = self.client.get(self.authors_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_book_api(self):
        """ამოწმებს წიგნის წაშლის API-ს (DELETE)"""
        detail_url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)