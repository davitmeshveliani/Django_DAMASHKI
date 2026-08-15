from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.myapp.models import Task
from apps.serializers.my_app_model_serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
)


class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. : APIView
# /~~~~~~~~~~~~~~~~~~~~~~~~~
class TaskListCreateView(APIView):
    def get(self, request):
        tasks = Task.objects.all().order_by('-created_at')

        day_param = request.query_params.get('day', None)
        if day_param:
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            day_lower = day_param.strip().lower()
            if day_lower in days:
                tasks = tasks.filter(deadline__week_day=days.index(day_lower) + 1)

        paginator = TaskPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request, view=self)

        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)



    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskCreateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskCreateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. დაკომენტარებული ალტერნატივა: GENERICS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# class TaskListCreateView(generics.ListCreateAPIView):
#     queryset = Task.objects.all().order_by('-created_at')
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#
#     filterset_fields = ['status', 'deadline']
#     search_fields = ['title', 'description']
#
#     ordering_fields = ['created_at']
#     ordering = ['-created_at']
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return TaskCreateSerializer
#         return TaskSerializer
#
#
# class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ['PUT', 'PATCH']:
#             return TaskCreateSerializer
#         return TaskDetailSerializer


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3. დაკომენტარებული ალტერნატივა: VIEWSET
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# from rest_framework import viewsets
#
# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return TaskCreateSerializer
#         elif self.request.method in ['PUT', 'PATCH']:
#             return TaskCreateSerializer
#         return TaskDetailSerializer