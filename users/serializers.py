from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'author_pseudonym']

    def create(self, validated_data):
        """
        Creates a new User and a new user_profile object at the same time
        :param validated_data:
        :return: UserProfile
        """
        user_data = validated_data.pop('user')
        author_pseudonym = validated_data.pop('author_pseudonym', None)
        user = UserSerializer().create(user_data)
        profile = UserProfile.objects.create(user=user, author_pseudonym=author_pseudonym)
        return profile