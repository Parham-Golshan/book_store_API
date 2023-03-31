from rest_framework import serializers
from .models import Book
from django.core.files import File
import io
import os
from urllib.request import urlopen
from book_store import settings


class BookSerializer(serializers.ModelSerializer):
    # Define author and author_pseudonym as read-only fields
    author = serializers.ReadOnlyField(source='author.user.username')
    author_pseudonym = serializers.ReadOnlyField(source='author.author_pseudonym')
    cover_image = serializers.ImageField(max_length=None, use_url=True, required=False)

    MAX_COVER_IMAGE_SIZE = 1 * 1024 * 1024  # 1 MB in bytes
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
                file_path = data['cover_image']
                if not os.path.isfile(file_path):
                    # Convert the path to a file object
                    file_path = os.path.join(settings.BASE_DIR, data['cover_image'])
                    file_path = os.path.abspath(file_path)
                with open(file_path, 'rb') as f:
                    stream = io.BytesIO(f.read())
                data['cover_image'] = File(stream, name=os.path.basename(file_path))
        elif cover_image:
            data['cover_image'] = cover_image
        return super().to_internal_value(data)

    def validate(self, data):
        # Check if an image is provided
        image = data.get('cover_image')
        if image:
            # Get the image size
            image_size = image.size

            # Check if the image size is too large
            if image_size > self.MAX_COVER_IMAGE_SIZE:
                raise serializers.ValidationError(f"The cover_image size is too large. "
                                                  f"Maximum allowed size is: {self.MAX_COVER_IMAGE_SIZE // 1000} KB")
        return data
