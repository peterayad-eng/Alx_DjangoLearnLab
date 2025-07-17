from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Function-based view for listing all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view for displaying library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register.as_view(), name='register'),

    # Role-based URLs
    path('admin/', views.Admin, name='admin_view'),
    path('librarian/', views.Librarian, name='librarian_view'),
    path('member/', views.Member, name='member_view'),

    # Function-based view URLs
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]

