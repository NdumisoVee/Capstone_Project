from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
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


# HTML
def login_view(request):
    return render(request, 'reviews/login.html')


def home_view(request):
    return render(request, 'reviews/index.html')


def movie_detail_view(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    reviews = Review.objects.filter(movie_title=movie)
    return render(request, 'reviews/movie_detail.html', {'movie': movie, 'reviews': reviews})


def submit_review(request):
    # Check if the user is authenticated before allowing review submission
    if not request.user.is_authenticated:
        # If the user is not authenticated, return a forbidden response or redirect them to login
        return HttpResponseForbidden("You must be logged in to submit a review.")

    # Handle the form submission
    if request.method == 'POST':
        movie_title = request.POST.get('movie_title')
        rating = request.POST.get('rating')
        review_content = request.POST.get('review_content')

        # Create a new review and associate it with the current user
        review = Review.objects.create(
            user=request.user,
            movie_title=movie_title,
            rating=rating,
            review_content=review_content,
        )

        # Add a success message
        messages.success(request, 'Review submitted successfully!')
        return redirect('reviews/submit_review')  # Redirect to the same page or another page as needed

    # Render the review submission form
    return render(request, 'reviews/submit_review.html')
