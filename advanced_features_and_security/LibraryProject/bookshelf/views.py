from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required , login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Book
from .forms import BookForm

# Create your views here.
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('view_books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form , 'action': 'Create'})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('view_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit', 'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('view_books')

    return render(request, 'bookshelf/confirm_delete.html', {'book': book})

