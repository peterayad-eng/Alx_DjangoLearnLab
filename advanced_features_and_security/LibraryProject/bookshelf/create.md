# Create a Book Instance

This documents clarify the steps and the expected output for creating a new book instance in Django using the ORM.

## Create a new instance command

```python
from .models import Book

# Creating the Book instance
new_book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Verifying the creation by printing
print(new_book)
```

## Expected Output

1984 by George Orwell (1949)

