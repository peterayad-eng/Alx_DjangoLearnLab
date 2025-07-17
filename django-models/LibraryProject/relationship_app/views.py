from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Book
from .models import Library
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Prefetch related books with their authors
        context['library'].books.select_related('author').all()
        return context

class register(CreateView):
    form_class = UserCreationForm()
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

class LoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/relationship_app/books/'

@login_required
def LogoutView(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

# Role checking functions
def is_admin(user):
    """Check if user has Admin role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Check if user has Librarian role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Check if user has Member role"""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def Admin(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def Librarian(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_librarian)
def Member(request):
    return render(request, 'relationship_app/member_view.html')

