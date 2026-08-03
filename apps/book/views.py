from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.book.models import Book
from apps.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer


  @action(detail=False, methods=['get'])
  def stats(self, request):
    stats_data = Book.objects.aggregate(
        total_books=Count('id'),
        older_books=Count('id', filter=Q(published_date__year__lt=2020)),
    )

    # 2.  (Group By 'author'  'genre' )

    genre_counts_queryset = (
        Book.objects.values('genre')
        .annotate(count=Count('id'))
        .order_by('genre')
    )

    genre_counts = {
        item['genre']: item['count']
        for item in genre_counts_queryset
        if item['genre']
    }

    data = {
        'total_books': stats_data['total_books'],
        'older_books': stats_data['older_books'],
        'genre_counts': genre_counts,
    }
    return Response(data, status=status.HTTP_200_OK)