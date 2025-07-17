from django.urls import path
from .views import book_list
from .views import LibraryDetailView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Function-based view for listing all books
    path('books/', book_list, name='list_books'),
    
    # Class-based view for displaying library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register.as_view(), name='register'),

    # Role-based URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),

]

