from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from .models import Category, Task, Subtask
from .serializers import CategorySerializer, TaskSerializer, SubtaskSerializer



class AppCursorPagination(CursorPagination):
    page_size = 4
    ordering = '-id'


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = AppCursorPagination

    def get_queryset(self):
        return Category.objects.all().prefetch_related('tasks__subtasks').order_by('-id')

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, *args, **kwargs):
        category = self.get_object()
        tasks_count = category.tasks.count()
        return Response(
            {
                "category_id": category.id,
                "category_name": category.name,
                "tasks_count": tasks_count
            },
            status=status.HTTP_200_OK
        )


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = AppCursorPagination

    def get_queryset(self):
        return Task.objects.all().select_related('category').prefetch_related('subtasks').order_by('-id')

    def perform_destroy(self, instance):
        instance.delete()


class SubtaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubtaskSerializer
    pagination_class = AppCursorPagination

    def get_queryset(self):
        return Subtask.objects.all().select_related('task').order_by('-id')

    def perform_destroy(self, instance):
        instance.delete()