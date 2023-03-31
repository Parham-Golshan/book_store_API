from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Book
from users.models import UserProfile
from traceback import format_exc
from decimal import Decimal
from django.urls import reverse
from .serializers import BookSerializer


book_detail_url = lambda pk: reverse('book-detail', args=[pk])


class BookTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user, author_pseudonym='Test Author')

        # create a test book
        self.book = Book.objects.create(
            title='Test Book',
            description='Test description',
            price=9.99,
            author=self.user_profile,
        )
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_create_book(self):
        url = reverse('book-list')
        # create a new book
        payload = {
            'title': 'New Book',
            'description': 'New description',
            'price': 14.99,
            'author': self.user_profile,
        }
        try:
            response = self.client.post(url, payload)
        except Exception:
            print(f"error = {format_exc()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, 'New Book')
        self.assertEqual(Book.objects.last().description, 'New description')
        self.assertEqual(Book.objects.last().price, Decimal('14.99'))
        self.assertEqual(Book.objects.last().author, self.user_profile)

    def test_list_books(self):
        url = reverse('book-list')
        # list all books
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], self.book.title)
        self.assertEqual(response.data['results'][0]['description'], self.book.description)
        self.assertEqual(response.data['results'][0]['price'], str(self.book.price))
        self.assertEqual(response.data['results'][0]['author_pseudonym'], self.user_profile.author_pseudonym)

    def test_book_detail(self):
        """
        Test that we can retrieve a single book by its ID
        """
        response = self.client.get(reverse('book-detail', args=[self.book.pk]))
        book_serializer = BookSerializer(instance=self.book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, book_serializer.data)

    def test_book_detail_not_found(self):
        """
        Test that a 404 error is returned when attempting to retrieve a book that does not exist
        """
        url = reverse('book-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_book_detail_unauthenticated(self):
        """
        Test that an unauthenticated user CAN retrieve a book
        """
        self.client.logout()
        response = self.client.get(book_detail_url(self.book.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book_detail(self):
        # Issue a PUT request to update the detail of the created book
        data = {
            'title': 'Updated Test Book',
            'description': 'An updated test book for testing purposes',
            'price': '29.99'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(book_detail_url(self.book.pk), data)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the book detail returned in the response is correct
        self.assertEqual(response.data['title'], 'Updated Test Book')
        self.assertEqual(response.data['description'], 'An updated test book for testing purposes')
        self.assertEqual(response.data['price'], '29.99')
        self.assertEqual(response.data['author'], 'testuser')
        self.assertEqual(response.data['author_pseudonym'], 'Test Author')

        # Refresh the book from the database and check that its detail is updated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Test Book')
        self.assertEqual(self.book.description, 'An updated test book for testing purposes')
        self.assertEqual(self.book.price, Decimal('29.99'))

    def test_delete_book_detail(self):
        # Issue a DELETE request to delete the created book
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(book_detail_url(self.book.pk))

        # Check that the response status code is 204
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the book is no longer in the database
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_darth_vader_permission_denied(self):
        # create a request data dictionary with a user with the username "Darth Vader"
        darth_vader_user = User.objects.create(username='Darth Vader', password='testpassword')
        darth_vader_user_profile = UserProfile.objects.create(user=darth_vader_user, author_pseudonym=None)
        request_data = {
            "title": "New Book",
            "description": "New Book Description",
            "price": 5.99,
            "author": darth_vader_user_profile
        }
        self.client.force_authenticate(user=darth_vader_user)
        # attempt to create a new book object with the request data
        response = self.client.post(reverse('book-list'), request_data)
        # check that the response status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookThrottleTestCase(APITestCase):
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user, author_pseudonym='Test Author')

        # create a test book
        self.book = Book.objects.create(
            title='Test Book',
            description='Test description',
            price=9.99,
            author=self.user_profile,
        )

        # get access token
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser2', 'password': 'testpass'})
        self.token = response.data['access']

    def test_1_throttle_user_rate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # test user rate limit
        for i in range(31):
            url = reverse('book-list')
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_2_throttle_anon_rate(self):
        self.client.credentials()  # remove token, use anonymous credentials
        # test anonymous rate limit
        for i in range(15):
            url = reverse('book-list')
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)