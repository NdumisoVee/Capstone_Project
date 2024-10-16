from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Review, Movie, Comment


# Serializer for handling review data
class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Read-only field to display the username of the review's author

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'rating', 'review_content', 'created_date', 'username']

    def create(self, validated_data):
        # Automatically associates the review with the current user from the request context
        user = self.context['request'].user
        return Review.objects.create(user=user, **validated_data)


# Serializer for handling movie data
class MovieSerializer(serializers.ModelSerializer):
    # Nested serialization to include related reviews for a movie
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'reviews']  # Includes reviews for better context


# Serializer for handling user registration
class UserSerializer(serializers.ModelSerializer):
    # The password field is write-only to prevent it from being exposed in API responses
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Uses Django's built-in create_user method to ensure password hashing
        return User.objects.create_user(**validated_data)


# Serializer for handling comment data
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Displays the username of the comment's author

    class Meta:
        model = Comment
        fields = ['id', 'review', 'username', 'content', 'created_at']  # Includes associated review, author, and content details
