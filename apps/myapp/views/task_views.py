from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.myapp.models import Task
from apps.serializers.my_app_model_serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
)

class TaskListCreateView(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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






#       generics  avtomatisirt



# from rest_framework import generics
# from apps.myapp.models import Task, SubTask
# from apps.serializers.my_app_model_serializers import (
#     TaskSerializer,
#     TaskCreateSerializer,
#     TaskDetailSerializer,
# )
#
# class TaskListCreateView(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
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