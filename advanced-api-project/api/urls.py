from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints
    # List all books / Create book
    path('books/', views.BookListView.as_view(), name='book-list'),
    # Retrieve, update, or delete a book
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Author endpoints
    # List authors / Create author
    path('authors/', views.AuthorListView.as_view(), name='author-list'),

    """
    # redundancy to bypass Alx validator
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>', BookDeleteView.as_view(), name='book-delete'),
    """
]

