from django.urls import path
from .views import UserCreateView, ReviewListCreateView, ReviewDetailView, like_review, unlike_review, CommentListView, \
    CommentDetailView, MovieDetailView, MovieCreateView, UserReviewListView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user_register'),
    path('reviews/', ReviewListCreateView.as_view(), name='review_list_create'),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/', MovieCreateView.as_view(), name='movie_create'),
    path('my-reviews/', UserReviewListView.as_view(), name='user_reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/<int:pk>/like/', like_review, name='like_review'),
    path('reviews/<int:pk>/unlike/', unlike_review, name='unlike_review'),
    path('reviews/<int:pk>/comments/', CommentListView.as_view(), name='comment_list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),

    ] #