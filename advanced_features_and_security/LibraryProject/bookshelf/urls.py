from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book CRUD operations
    path('books/', views.view_books, name='book_list'),
    path('books/create/', views.create_book, name='book_create'),
    path('books/<uuid:book_id>/edit/', views.edit_book, name='book_edit'),
    path('books/<uuid:book_id>/delete/', views.edit_book, name='book_delete'),
]

