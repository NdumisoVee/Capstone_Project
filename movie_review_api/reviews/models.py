from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

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

    def __str__(self):
        return f"{self.movie_title} - {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f"{self.user.username} likes {self.review.movie.title}"
