from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from apps.book.models import BookCategory, BookTask, BookSubTask

class BookSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSubTask
        fields = ['id', 'task', 'title', 'description', 'status', 'deadline', 'created_at']

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    category = BookCategorySerializer(read_only=True)
    book_subtasks = BookSubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = BookTask
        fields = ['id', 'title', 'category', 'description', 'status', 'deadline', 'book_subtasks', 'created_at']


class BookTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTask
        fields = ['id', 'title', 'description', 'category', 'status', 'deadline']

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise ValidationError('Дата дедлайна не может быть в прошлом.')
        return value