from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from apps.book.models import BookAuthor, BookCategory, Book, BookTask, BookSubTask, CommonStatus


# ავტორის სერიალიზატორი
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ['id', 'name', 'bio']


# კატეგორიის სერიალიზატორი
class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ['id', 'name']


# წიგნის სერიალიზატორი ჩაშენებული (Nested) ავტორით
class BookSerializer(serializers.ModelSerializer):
    # ეს გამოიტანს ავტორის სრულ ობიექტს (JSON-ის სახით)
    author = AuthorSerializer(read_only=True)
    category = BookCategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'published_date', 'status', 'created_at']


# წიგნის დავალებების სერიალიზატორები
class BookTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTask
        fields = ['id', 'title', 'category', 'description', 'status', 'deadline', 'created_at']

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise ValidationError('Дата дедлайна не может быть в прошлом.')
        return value


class BookSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSubTask
        fields = ['id', 'task', 'title', 'description', 'status', 'deadline', 'created_at']


class BookAuthorSerializer:
    class Meta:
        model = BookAuthor
        fields = ['id', 'name', 'bio']

