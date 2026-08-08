from django.test import TestCase
from django.utils import timezone
import datetime
from rest_framework.test import APITestCase

from apps.book.models import BookAuthor, BookCategory, Book, BookTask, CommonStatus
from apps.book.serialisers.book_serializers import BookTaskCreateSerializer


class BookComprehensiveTests(APITestCase):

    def setUp(self):
        self.author = BookAuthor.objects.create(
            name="ვაჟა-ფშაველა",
            bio="კლასიკოსი მწერალი"
        )
        self.category = BookCategory.objects.create(
            name="პოემა"
        )
        self.future_deadline = timezone.now() + datetime.timedelta(days=7)
        self.past_deadline = timezone.now() - datetime.timedelta(days=2)

    def test_book_author_and_category_creation(self):
        """ამოწმებს ავტორისა და კატეგორიის სწორად შექმნას"""
        self.assertEqual(self.author.name, "ვაჟა-ფშაველა")
        self.assertEqual(str(self.author), "ვაჟა-ფშაველა")
        self.assertEqual(self.category.name, "პოემა")
        self.assertEqual(str(self.category), "პოემა")

    def test_book_model_with_relations(self):
        """ამოწმებს Book მოდელის შექმნას ავტორთან და კატეგორიასთან კავშირში"""
        book = Book.objects.create(
            title="ალუდა ქეთელაური",
            author=self.author,
            category=self.category,
            status=CommonStatus.PUBLISHED
        )
        self.assertEqual(book.title, "ალუდა ქეთელაური")
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.category, self.category)
        self.assertEqual(str(book), "ალუდა ქეთელაური")

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