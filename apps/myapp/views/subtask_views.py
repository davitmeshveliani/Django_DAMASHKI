from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.myapp.models import SubTask
from ..serialisers.home_serializers import SubTaskSerializer, SubTaskCreateSerializer

class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================================
# ავტომატური ჯენერიკები (დაკომენტარებული)
# ==========================================
# from rest_framework import generics
#
# class SubTaskListCreateView(generics.ListCreateAPIView):
#     queryset = SubTask.objects.all()
#     serializer_class = SubTaskCreateSerializer
#
# class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = SubTask.objects.all()
#     serializer_class = SubTaskCreateSerializer