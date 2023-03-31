from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from users.models import UserProfile
from users.serializers import UserProfileSerializer


class UserProfileCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        self.profile_data = {
            'user': self.user_data,
            'author_pseudonym': 'Test Author'
        }

    def test_create_user_profile(self):
        response = self.client.post(self.register_url, data=self.profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=self.user_data['username'])
        profile = UserProfile.objects.get(user=user)

        serializer = UserProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
