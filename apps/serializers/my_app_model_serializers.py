from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from apps.myapp.models import Category, Task, SubTask


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'categories', 'subtasks', 'status', 'deadline', 'created_at']


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']
        read_only_fields = ['created_at']

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise ValidationError('Дата дедлайна не может быть в прошлом.')
        return value


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise ValidationError({'name': 'Категория с таким названием уже существует.'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name and name != instance.name and Category.objects.filter(name=name).exists():
            raise ValidationError({'name': 'Категория с таким названием уже существует.'})
        return super().update(instance, validated_data)