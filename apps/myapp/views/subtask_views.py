from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from apps.myapp.models import SubTask
from apps.myapp.serialisers.home_serializers import SubTaskSerializer, SubTaskCreateSerializer


class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all().select_related('task').order_by('-id')

        task_name_param = request.query_params.get('task_name', None)
        status_param = request.query_params.get('status', None)

        if task_name_param:
            subtasks = subtasks.filter(task__title__icontains=task_name_param)
        if status_param:
            subtasks = subtasks.filter(status=status_param)

        paginator = SubTaskPagination()
        paginated_subtasks = paginator.paginate_queryset(subtasks, request, view=self)
        serializer = SubTaskSerializer(paginated_subtasks, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask.objects.select_related('task'), pk=pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 2: GENERICS


#
# class SubTaskListCreateView(generics.ListCreateAPIView):
#     pagination_class = SubTaskPagination
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#
#     filterset_fields = ['status', 'task']
#     search_fields = ['title', 'description']
#     ordering_fields = ['id', 'deadline']
#     ordering = ['-id']
#
#     def get_queryset(self):
#         queryset = SubTask.objects.all().select_related('task').order_by('-id')
#         task_name_param = self.request.query_params.get('task_name', None)
#         status_param = self.request.query_params.get('status', None)
#
#         if task_name_param:
#             queryset = queryset.filter(task__name__icontains=task_name_param)
#         if status_param:
#             queryset = queryset.filter(status=status_param)
#
#         return queryset
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return SubTaskCreateSerializer
#         return SubTaskSerializer
#
#
# class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = SubTask.objects.all().select_related('task')
#
#     def get_serializer_class(self):
#         if self.request.method in ['PUT', 'PATCH']:
#             return SubTaskCreateSerializer
#         return SubTaskSerializer

# 3.: VIEWSET
# from rest_framework import viewsets
#
# class SubTaskViewSet(viewsets.ModelViewSet):
#     pagination_class = SubTaskPagination
#
#     def get_queryset(self):
#         queryset = SubTask.objects.all().select_related('task').order_by('-id')
#         task_name_param = self.request.query_params.get('task_name', None)
#         status_param = self.request.query_params.get('status', None)
#
#         if task_name_param:
#             queryset = queryset.filter(task__name__icontains=task_name_param)
#         if status_param:
#             queryset = queryset.filter(status=status_param)
#
#         return queryset
#
#     def get_serializer_class(self):
#         if self.request.method in ['POST', 'PUT', 'PATCH']:
#             return SubTaskCreateSerializer
#         return SubTaskSerializer