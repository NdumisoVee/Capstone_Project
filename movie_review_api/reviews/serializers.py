from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import User


class ReviewSerializer(serializers.ModelSerializer):  # ReviewSerializer manages review data
    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(
    serializers.ModelSerializer):  # UserSerializer handles user data with password write-only functionality.
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
