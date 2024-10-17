from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review, Movie, Comment
from .serializers import ReviewSerializer, MovieSerializer, UserSerializer, CommentSerializer


# User Registration View
# Allows new users to register
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Review List and Create View
# Allows authenticated users to list and create reviews
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie_title', 'rating']  # Allows filtering by movie title and rating


# Review Detail View (Retrieve, Update, Delete)
# Allows users to view, update, or delete their own reviews
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        review = super().get_object()
        # Restrict updates and deletions to the review author
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and review.user != self.request.user:
            raise PermissionDenied("You do not have permission to modify or delete this review.")
        return review


# Movie Detail View
# Allows users to retrieve details of a specific movie
class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


# List Reviews by User
# Allows users to view all their own reviews
class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Returns only the reviews created by the authenticated user
        return Review.objects.filter(user=self.request.user)


# Create Movie View
# Allows authenticated users to create a new movie entry
class MovieCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Saves the movie data
        serializer.save()


# Views for liking and unliking reviews
# Like a review
def like_review(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    review = get_object_or_404(Review, pk=pk)

    if request.user in review.likes.all():
        return JsonResponse({'detail': 'Already liked this review'}, status=status.HTTP_400_BAD_REQUEST)

    # Add the like
    review.likes.add(request.user)
    return JsonResponse({'detail': 'Review liked'}, status=status.HTTP_200_OK)


# Unlike a review
def unlike_review(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    review = get_object_or_404(Review, pk=pk)

    if request.user not in review.likes.all():
        return JsonResponse({'detail': 'Not yet liked this review'}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the like
    review.likes.remove(request.user)
    return JsonResponse({'detail': 'Review unliked'}, status=status.HTTP_200_OK)


# Comment List Create View
# Allows users to list all comments and create new ones
class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a comment
        serializer.save(user=self.request.user)


# Comment Detail View (Retrieve, Update, Delete)
# Allows users to retrieve, update, or delete a specific comment
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        comment = super().get_object()
        # Allow the comment owner to delete or update their comment, but anyone can view it.
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and comment.user != self.request.user:
            raise PermissionDenied("You do not have permission to modify or delete this comment.")
        return comment
