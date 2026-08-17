from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination

from apps.book.models import BookTask, BookSubTask, BookAuthor
from apps.serializers.my_book_model_serializers import (
    BookTaskSerializer,
    BookTaskCreateSerializer,
    BookSubTaskSerializer,
    BookAuthorSerializer,
)


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookTaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookTaskSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return BookTask.objects.select_related('category').prefetch_related('book_subtasks').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookTaskCreateSerializer
        return BookTaskSerializer


class BookTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookTaskSerializer

    def get_queryset(self):
        return BookTask.objects.select_related('category').prefetch_related('book_subtasks').all()


class BookSubTaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookSubTaskSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return BookSubTask.objects.select_related('task').all()


class BookSubTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSubTaskSerializer

    def get_queryset(self):
        return BookSubTask.objects.select_related('task').all()


class BookAuthorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookAuthorSerializer
    queryset = BookAuthor.objects.all()
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class BookAuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookAuthorSerializer
    queryset = BookAuthor.objects.all()