from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.myapp.models import Category, Task, SubTask
from apps.serializers import CategorySerializer, TaskSerializer, SubTaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_tasks = Task.objects.count()

        status_counts = {}
        for status_choice in Task.objects.values_list('status', flat=True).distinct():
            if status_choice:
                status_counts[status_choice] = Task.objects.filter(status=status_choice).count()

        now = timezone.now()
        overdue_tasks = Task.objects.filter(deadline__lt=now).exclude(status='Done').count()

        data = {
            'total_tasks': total_tasks,
            'status_counts': status_counts,
            'overdue_tasks': overdue_tasks
        }
        return Response(data, status=status.HTTP_200_OK)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer