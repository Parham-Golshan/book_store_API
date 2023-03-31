from django.urls import path
from .views import UserProfileCreate, UserBookList

urlpatterns = [
    path('register/', UserProfileCreate.as_view(), name='register'),
    path('published-books/', UserBookList.as_view(), name='published-books')
    ]
