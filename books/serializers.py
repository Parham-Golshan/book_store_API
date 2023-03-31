from rest_framework import serializers
from .models import Book
from django.core.files import File
import io
import os
from urllib.request import urlopen


class BookSerializer(serializers.ModelSerializer):
    # Define author and author_pseudonym as read-only fields
    author = serializers.ReadOnlyField(source='author.user.username')
    author_pseudonym = serializers.ReadOnlyField(source='author.author_pseudonym')
    cover_image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'cover_image', 'price', 'author', 'author_pseudonym']
        # read_only_fields = ['id', 'author', 'author_pseudonym']

    def to_internal_value(self, data: dict) -> dict:
        """
        Convert the path to the image or URL to the image to a file object for the serializer to handle.
        If the cover image is a file which is being sent via form-data, it will serialize the file too.

        Args:
            data (dict): The data to be validated and deserialized.

        Returns:
            dict: The validated and deserialized data.
        """
        cover_image = data.get('cover_image', None)
        if 'cover_image' in data and isinstance(data['cover_image'], str):
            if cover_image.startswith('http'):
                # Download the image from the URL
                response = urlopen(cover_image)
                file_name = os.path.basename(cover_image)
                stream = io.BytesIO(response.read())
                data['cover_image'] = File(stream, name=file_name)
            else:
                # Remove leading forward slash from cover_image path
                data['cover_image'] = data['cover_image'].lstrip('/')
                # Convert the path to a file object
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', data['cover_image']))
                with open(file_path, 'rb') as f:
                    stream = io.BytesIO(f.read())
                data['cover_image'] = File(stream, name=os.path.basename(file_path))
        elif cover_image:
            data['cover_image'] = cover_image
        return super().to_internal_value(data)