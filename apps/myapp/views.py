from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.myapp.models import Category, SubTask, Task
from apps.serializers import (
    CategorySerializer,
    SubTaskSerializer,
    TaskSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  @action(detail=False, methods=['get'])
  def stats(self, request):
    now = timezone.now()

    # 1. (aggregate)

    stats_data = Task.objects.aggregate(
        total_tasks=Count('id'),
        overdue_tasks=Count(
            'id', filter=Q(deadline__lt=now) & ~Q(status='Done')
        ),
    )

    # 2. (annotate / Group By status)

    status_counts_queryset = (
        Task.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )

    status_counts = {
        item['status']: item['count']
        for item in status_counts_queryset
        if item['status']
    }

    data = {
        'total_tasks': stats_data['total_tasks'],
        'status_counts': status_counts,
        'overdue_tasks': stats_data['overdue_tasks'],
    }
    return Response(data, status=status.HTTP_200_OK)


class SubTaskViewSet(viewsets.ModelViewSet):
  queryset = SubTask.objects.all()
  serializer_class = SubTaskSerializer