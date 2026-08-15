from rest_framework import serializers
from apps.book.models import BookAuthor

class BookAuthorSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='book-author-detail',
        lookup_field='pk'
    )

    class Meta:
        model = BookAuthor
        fields = ['id', 'name', 'bio']

class BookAuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ['id', 'name', 'bio']

