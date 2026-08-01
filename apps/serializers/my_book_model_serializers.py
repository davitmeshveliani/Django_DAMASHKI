from rest_framework import serializers
from apps.book.models import Book, BookAuthor

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = ['id', 'name', 'bio']

class BookSerializer(serializers.ModelSerializer):
    # ეს გამოიტანს ავტორის სრულ ობიექტს (JSON-ის სახით)
    author = AuthorSerializer(read_only=True)

    # ალტერნატივა: თუ გინდა ავტორის ID-ს მიღება/გაგზავნა
    # author = serializers.PrimaryKeyRelatedField(queryset=BookAuthor.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'status']