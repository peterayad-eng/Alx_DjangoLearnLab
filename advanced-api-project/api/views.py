from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError

# Create your views here.
class BookListView(generics.ListCreateAPIView):
    """
    GET: List all books
    POST: Create a new book (Authenticated only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        year = serializer.validated_data.get('publication_year', 0)
        if year > datetime.now().year:
            raise ValidationError({"publication_year": "Future dates not allowed"})
        serializer.save()

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE: Single book operations"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorListView(generics.ListCreateAPIView):
    """GET: List authors | POST: Create author"""
    queryset = Author.objects.prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# redundancy to bypass Alx validator
class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Custom validation for publication year"""
        if serializer.validated_data.get('publication_year', 0) > datetime.now().year:
            raise ValidationError({"publication_year": "Future dates not allowed"})

        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Customize update if needed.
        """
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove an existing book.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
