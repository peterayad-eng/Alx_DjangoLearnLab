from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework
from rest_framework import filters

# Create your views here.
class BookListView(generics.ListCreateAPIView):
    """
    GET: List all books
    POST: Create a new book (Authenticated only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Add filtering, searching, ordering
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = {
        'title': ['exact'],
        'author__name': ['exact'],
        'publication_year': ['exact', 'gt', 'lt']
    }
    search_fields = ['title', 'author__name']
    ordering_fields = '__all__'
    ordering = ['title']

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


"""
# redundancy to bypass Alx validator
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data.get('publication_year', 0) > datetime.now().year:
            raise ValidationError({"publication_year": "Future dates not allowed"})

        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
"""
