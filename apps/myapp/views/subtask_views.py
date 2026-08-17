from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.myapp.models import SubTask
from apps.myapp.serialisers.home_serializers import SubTaskSerializer, SubTaskCreateSerializer


class SubTaskLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all().select_related('task').order_by('-id')

        task_name_param = request.query_params.get('task_name', None)
        status_param = request.query_params.get('status', None)

        if task_name_param:
            subtasks = subtasks.filter(task__title__icontains=task_name_param)
        if status_param:
            subtasks = subtasks.filter(status=status_param)

        paginator = SubTaskLimitOffsetPagination()
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