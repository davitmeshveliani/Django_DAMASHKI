from rest_framework import serializers
from apps.book.models import BookCategory, BookAuthor, Book, BookTask, BookSubTask

# --- Category & Author ---
class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ['id', 'name']

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ['id', 'name', 'bio']


class BookSerializer(serializers.ModelSerializer):
    author = BookAuthorSerializer(read_only=True)
    category = BookCategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'published_date', 'status', 'created_at']

class BookDetailSerializer(serializers.ModelSerializer):
    author = BookAuthorSerializer(read_only=True)
    category = BookCategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'published_date', 'status', 'created_at', 'updated_at']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'published_date', 'status']


class BookTaskSerializer(serializers.ModelSerializer):
    category = BookCategorySerializer(read_only=True)

    class Meta:
        model = BookTask
        fields = ['id', 'title', 'description', 'category', 'status', 'deadline', 'created_at']

class BookTaskDetailSerializer(serializers.ModelSerializer):
    category = BookCategorySerializer(read_only=True)
    book_subtasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = BookTask
        fields = ['id', 'title', 'description', 'category', 'status', 'deadline', 'book_subtasks', 'created_at']

class BookTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTask
        fields = ['id', 'title', 'description', 'category', 'status', 'deadline']


class BookSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']

class BookSubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline']