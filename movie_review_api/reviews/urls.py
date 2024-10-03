from django.urls import path
from .views import UserCreateView, ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user_register'),
    path('reviews/', ReviewListCreateView.as_view(), name='review_list_create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),

    ]