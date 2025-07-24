import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clear existing data to avoid duplicates on re-run
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")

# Create books
book1 = Book.objects.create(title="Harry Potter", author=author1)
book2 = Book.objects.create(title="1984", author=author2)

# Create library
library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

# Create librarian
librarian = Librarian.objects.create(name="Alice", library=library)

print("--- Sample Data Created ---")

# Query all books by a specific author
print("\n--- Query all books by J.K. Rowling ---")
author_name = "J.K. Rowling"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
for book in books_by_author:
    print(f"- {book.title}")

# List all books in a library
print("\n--- List all books in Central Library ---")
library_name = "Central Library"
library = Library.objects.get(name=library_name)
for book in library.books.all():
    print(f"- {book.title}")

# Retrieve the librarian for a library
print("\n--- Retrieve the librarian for Community Library ---")
community_library = Library.objects.get(name="Community Library")
librarian = Librarian.objects.get(library=community_library)
print(f"- {librarian.name}")

