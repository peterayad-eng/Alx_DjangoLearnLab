from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime
from .models import Author, Book

# Create your tests here.
class BookAPITests(APITestCase):
    """Tests for Book API endpoints"""
    
    def setUp(self):
        # Test data
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        
        # Existing book for detail/update/delete tests
        self.book = Book.objects.create(
            title="Existing Book",
            publication_year=2020,
            author=self.author
        )
        
        # Valid payload
        self.valid_data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        
        # URLs
        self.list_url = '/api/books/'
        self.detail_url = f'/api/books/{self.book.id}/'

    # --- LIST/CREATE TESTS ---
    def test_get_all_books(self):
        """Anyone can view book list"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_authenticated_user_can_create_book(self):
        """Authenticated POST creates a book"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_unauthenticated_user_cannot_create_book(self):
        """Unauthenticated users get 403"""
        response = self.client.post(self.list_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_validation(self):
        """Future publication year should fail"""
        self.client.force_authenticate(user=self.user)
        invalid_data = self.valid_data.copy()
        invalid_data["publication_year"] = datetime.now().year + 1
        
        response = self.client.post(self.list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

    # --- DETAIL VIEW TESTS ---
    def test_get_single_book(self):
        """Anyone can view single book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_authenticated_user_can_update_book(self):
        """Authenticated PUT/PATCH updates book"""
        self.client.force_authenticate(user=self.user)
        updated_data = {"title": "Updated Title"}
        
        # Test PATCH
        response = self.client.patch(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_authenticated_user_can_delete_book(self):
        """Authenticated DELETE removes book"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

class AuthorAPITests(APITestCase):
    """Tests for Author API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.author = Author.objects.create(name="Existing Author")
        self.url = '/api/authors/'
        self.valid_data = {"name": "New Author"}

    def test_get_all_authors(self):
        """Anyone can view author list"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_author_authenticated(self):
        """Authenticated users can create authors"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
