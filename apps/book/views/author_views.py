from rest_framework import generics
from apps.book.models import BookAuthor
from apps.book.serialisers.book_serializers import AuthorSerializer


class BookAuthorListCreateView(generics.ListCreateAPIView):
    """ავტორების სია (GET) და ახალი ავტორის შექმნა (POST)"""
    queryset = BookAuthor.objects.all()
    serializer_class = AuthorSerializer


class BookAuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """კონკრეტული ავტორის ნახვა (GET), განახლება (PUT/PATCH) და წაშლა (DELETE)"""
    queryset = BookAuthor.objects.all()
    serializer_class = AuthorSerializer