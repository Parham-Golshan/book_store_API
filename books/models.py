from django.db import models
from users.models import UserProfile


class Book(models.Model):
    author = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_images', null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.title} Book"
