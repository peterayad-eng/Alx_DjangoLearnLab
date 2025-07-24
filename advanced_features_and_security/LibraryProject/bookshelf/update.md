# Update the Book instance title

This documents clarify the steps and the expected output for updating the retrieved book instance in Django using the ORM.

## Update instance command

```python
from .models import Book

updated_book = Book.objects.get(title="1984")
updated_book.title = "Nineteen Eighty-Four"
updated_book.save()
print(updated_book)
```

## Expected output

Nineteen Eighty-Four by George Orwell (1949)

