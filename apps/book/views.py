from rest_framework import viewsets
from apps.book.models import Book
from apps.serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer