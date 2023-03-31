from rest_framework.generics import CreateAPIView, ListAPIView
from .models import UserProfile
from .serializers import UserProfileSerializer
from books.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from rest_framework.throttling import UserRateThrottle
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

class UserProfileCreate(CreateAPIView):
    serializer_class = UserProfileSerializer
    renderer_classes = [JSONRenderer, XMLRenderer]
    throttle_classes = [UserRateThrottle]


class UserBookList(ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a list of books published by the authenticated user.
        Only books that have been published by the user making the request will be returned.

            :return: A queryset of books published by the authenticated user.
            :rtype: QuerySet
        """
        user = self.request.user
        return Book.objects.filter(author__user=user)

    @swagger_auto_schema(
        operation_description="""Retrieves userprofile detail and user books **by ID of the user** 
        **Authorization **IS** required** for this method""",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)