from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime
from .models import Author, Book
from django.urls import reverse

class BookAPITests(APITestCase):
    """Tests for Book API endpoints"""

    def setUp(self):
        # Test data
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass'
        )
        self.author = Author.objects.create(name="Test Author")

        # Existing book for detail/update/delete tests
        self.book = Book.objects.create(
            title="Existing Book",
            publication_year=2020,
            author=self.author
        )

        # URLs
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.id})

    # --- Authentication Tests ---
    def test_unauthenticated_access(self):
        """Test unauthenticated user permissions"""
        # Should be able to GET
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should NOT be able to POST
        response = self.client.post(self.list_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- CRUD Tests ---
    def test_authenticated_user_can_create_book(self):
        """Authenticated users can create books"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_get_single_book(self):
        """Anyone can view a single book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Existing Book")

    def test_update_book(self):
        """Authenticated users can update books"""
        self.client.login(username='testuser', password='testpass123')
        updated_data = {"title": "Updated Title"}
        response = self.client.patch(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        """Only admins can delete books"""
        # Regular user can't delete
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin can delete
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # --- Validation Tests ---
    def test_create_book_validation(self):
        """Test publication year validation"""
        self.client.login(username='testuser', password='testpass123')
        invalid_data = {
            "title": "Future Book",
            "publication_year": datetime.now().year + 1,
            "author": self.author.id
        }
        response = self.client.post(self.list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

class AuthorAPITests(APITestCase):
    """Tests for Author API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Existing Author")
        self.url = reverse('author-list')
        self.detail_url = reverse('author-detail', kwargs={'pk': self.author.id})

    def test_create_author(self):
        """Authenticated users can create authors"""
        self.client.login(username='testuser', password='testpass123')
        data = {"name": "New Author"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_get_authors(self):
        """Anyone can view authors"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

