from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.book.models import BookAuthor, BookCategory, Book, CommonStatus


class BookAPIViewsTests(APITestCase):

    def setUp(self):
        self.author = BookAuthor.objects.create(
            name="გალაკტიონ ტაბიძე",
            bio="გენიალური პოეტი"
        )
        self.category = BookCategory.objects.create(
            name="ლექსები"
        )
        self.book = Book.objects.create(
            title="არტისტული ყვავილები",
            author=self.author,
            category=self.category,
            status=CommonStatus.PUBLISHED
        )
        self.authors_url = reverse('book-author-list-create')
        self.books_url = reverse('book-list-create')

    def test_get_authors_list(self):
        """ამოწმებს ავტორების სიის წამოღებას (GET)"""
        response = self.client.get(self.authors_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_books_list(self):
        """ამოწმებს წიგნების სიის წამოღებას (GET)"""
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "არტისტული ყვავილები")

    def test_delete_book(self):
        """ამოწმებს წიგნის წაშლას (DELETE)"""
        detail_url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)