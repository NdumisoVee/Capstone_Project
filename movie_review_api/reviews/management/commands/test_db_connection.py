from django.core.management.base import BaseCommand
from reviews.models import Review, Movie
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Test the MySQL database connection by creating and listing sample data.'

    def handle(self, *args, **kwargs):
        # Creating a test user
        user, _ = User.objects.get_or_create(username='Ndumiso', email='ndumiso_v@icloud.com')

        # Creating a test movie
        movie, _ = Movie.objects.get_or_create(title='The Lion King',
                                               description='An animated, musical/drama feature film')

        # Creating a test review
        review, created = Review.objects.get_or_create(
            movie_title=movie,
            user=user,
            review_content="Awesome, very funny and emotional",
            rating=4,
        )

        if created:
            self.stdout.write(f"Created new review for {movie.title} by {user.username}")
        else:
            self.stdout.write(f"Review already exists for {movie.title} by {user.username}")

        # List all reviews
        reviews = Review.objects.all()
        for review in reviews:
            self.stdout.write(str(review))
