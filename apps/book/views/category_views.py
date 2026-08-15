from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from apps.book.models import BookCategory
from apps.serializers.my_book_model_serializers import BookCategorySerializer

class BookCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    pagination_class = PageNumberPagination