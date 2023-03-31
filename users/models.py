from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_pseudonym = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
