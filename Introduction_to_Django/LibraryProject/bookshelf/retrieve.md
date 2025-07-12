# Retrieve the Book instance

This documents clarify the steps and the expected output for retrieving a book instance in Django using the ORM.

## Retrieve instance command

```python
from bookshelf.models import Book

retrieved_book = Book.objects.get(title="1984")
print(retrieved_book)
```

## Expected output

1984 by George Orwell (1949)

