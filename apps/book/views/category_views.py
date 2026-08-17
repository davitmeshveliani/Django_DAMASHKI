from rest_framework import generics, filters
from apps.book.models import BookCategory
from apps.serializers.my_book_model_serializers import BookCategorySerializer
from apps.book.views.book_viewset_views import CustomPagination

class BookCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']


class BookCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer