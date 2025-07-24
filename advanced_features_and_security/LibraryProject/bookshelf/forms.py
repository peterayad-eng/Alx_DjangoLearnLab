from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'publication_year': 'Year of Publication'
        }
        widgets = {
            'publication_year': forms.NumberInput(attrs={'min': 0, 'max': 9999}),
        }

