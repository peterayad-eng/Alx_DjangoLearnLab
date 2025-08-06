from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents an author with a name field.
    Related to Book via one-to-many relationship.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a book with title, publication year,
    and foreign key to Author model.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

