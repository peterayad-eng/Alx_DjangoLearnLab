from django.urls import path
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    # Function-based view for listing all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view for displaying library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView, name='register'),
]

