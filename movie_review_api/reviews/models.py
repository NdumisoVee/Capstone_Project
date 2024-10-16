from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='No description available')
    release_date = models.DateField(default='2000-01-01')

    def __str__(self):
        return self.title


# Movie Title, Review Content, Rating, User, and Created Date are defined.
class Review(models.Model):
    movie_title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews')  # ForeignKey to User ensures reviews are tied to specific users.
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)

    def __str__(self):
        return f"{self.movie_title} - {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_for_review')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes_for_review')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review') # Ensures that a user can like a review only once

    def __str__(self):
        return f"{self.user.username} likes {self.review.movie.title}"


class Comment(models.Model):
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)