from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing CRUD operations on Books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # method to track who added the book
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

