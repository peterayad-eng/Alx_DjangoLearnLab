from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView, ListView
from .models import Book
from .models import Library
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
def book_list(request):
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

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

class login_view(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/relationship_app/books/'

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

