from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model data with validation for publication_year.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author data including nested Book objects.
    Dynamically includes all books by the author.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

