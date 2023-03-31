from .models import Book
from rest_framework import generics
from .serializers import BookSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Handling response content type based on the request Accept header
    renderer_classes = [JSONRenderer, XMLRenderer]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # parser_classes = [FormParser, MultiPartParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__user__username', 'price', 'author__author_pseudonym']

    def get_queryset(self):
        """
        Override the default queryset to filter based on query params

        Supported query parameters:
            price__lt: Return books with price less than the specified value.
            price__gt: Return books with price greater than the specified value.
            title: Return books with a title that contains the specified string.
            author: Return books written by the specified user.
            author_pseudonym: Return books written by the specified author pseudonym.

        Returns:
            A filtered queryset based on the query parameters.
        """
        queryset = super().get_queryset()
        # Creating a dictionary of all the filters we want to apply.
        search_filters = {
            'price__lt': self.request.query_params.get('price__lt'),
            'price__gt': self.request.query_params.get('price__gt'),
            'title': self.request.query_params.get('title'),
            'author__user__username': self.request.query_params.get('author'),
            'author__author_pseudonym': self.request.query_params.get('author_pseudonym'),
        }
        # Removing any filters with None values.
        search_filters = {k: v for k, v in search_filters.items() if v is not None}
        queryset = queryset.filter(**search_filters)
        return queryset

    def perform_create(self, serializer):
        username = self.request.user.username
        author_pseudonym = self.request.user.userprofile.author_pseudonym
        # Creating exception for Darth Vader
        if username == "Darth Vader" or author_pseudonym == "Darth Vader":
            raise PermissionDenied("Unfortunately You cannot publish your work!")
        # Adding author to the book object
        serializer.save(author=self.request.user.userprofile)

    # Add Swagger documentation here
    @swagger_auto_schema(
        operation_description="""Get List of the Books. You can use query params to **filter** the response:
                              There are 2 options:
                              - Using \'**search**\' as key
                              - Using **price__lt**, **price__gt**, **title**, **author**, **author_pseudonym** as key(s)""",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY,
                              description="Search books by title, author username, author pseudonym or price",
                              type='string'),
            openapi.Parameter('price__lt', openapi.IN_QUERY, description="Filter by price less than",
                              type='float | integer'),
            openapi.Parameter('price__gt', openapi.IN_QUERY, description="Filter by price greater than",
                              type='float | integer'),
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter by book title", type='string'),
            openapi.Parameter('author', openapi.IN_QUERY, description="Filter by author username", type='string'),
            openapi.Parameter('author_pseudonym', openapi.IN_QUERY, description="Filter by author pseudonym",
                              type='string'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BookSerializer(many=True),
        operation_description="""Create a new book. You can send the **cover_image** by its **url** or **file path** if using a 
        json body. It is also possible to send the image **file** via form-data in postman""",
        manual_parameters=[
            openapi.Parameter('cover_image', openapi.IN_QUERY, description="Cover image file",
                              type='string (URL or file_path) | file'),
            openapi.Parameter('price', openapi.IN_QUERY, description="Book price (**required**)",
                              type='float | integer'),
            openapi.Parameter('title', openapi.IN_QUERY, description="Title of the book (**required**)",
                              type='string'),
            openapi.Parameter('description', openapi.IN_QUERY, description="Description of the book",
                              type='string')
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Handling response content type based on the request Accept header
    renderer_classes = [JSONRenderer, XMLRenderer]
    # Only Authenticated users for non GET/HEAD/OPTIONS requests, and only owner (Author) of the book for those requests
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieves a book by its ID. **Authorization is **NOT** required** for this method",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)