# Delete the Book instance

This documents clarify the steps for deleting the retrieved book instance in Django using the ORM.

## Delete instance command

```python
from bookshelf.models import Book

deleted_book = Book.objects.get(title="Nineteen Eighty-Four")
deleted_book.delete()
```

