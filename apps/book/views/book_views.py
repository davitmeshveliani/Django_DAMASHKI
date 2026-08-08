from rest_framework import generics
from apps.book.models import Book, BookAuthor
from apps.book.serialisers.book_serializers import BookSerializer, BookAuthorSerializer

# ავტორებისთვის: სია (GET) და შექმნა (POST)
class BookAuthorListCreateView(generics.ListCreateAPIView):
    queryset = BookAuthor.objects.all()
    serializer_class = BookAuthorSerializer

# ავტორებისთვის: დეტალური ნახვა, რედაქტირება და წაშლა (GET, PUT, PATCH, DELETE)
class BookAuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookAuthor.objects.all()
    serializer_class = BookAuthorSerializer

# წიგნებისთვის: სია და შექმნა
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# წიგნებისთვის: დეტალური ნახვა, რედაქტირება და წაშლა
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer