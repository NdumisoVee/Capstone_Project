The Movie Review API is a RESTful web service built using Django and Django REST Framework. 
It allows users to manage reviews for movies, including creating, reading, updating, and deleting reviews.
The API includes user authentication and authorization, ensuring that users can only modify their own reviews.


**Key Features**
User Authentication: Secure user authentication using Django's authentication system. Only registered users can create, update, or delete reviews.
Review Management (CRUD): Users can perform Create, Read, Update, and Delete operations on movie reviews.
Filter and Search: Filter reviews by movie_title and rating.
Pagination: Paginate review listings to manage large datasets efficiently.
Role-Based Access: Users can only edit or delete their own reviews, ensuring data integrity.

**Endpoints
Authentication**
Register: POST /auth/register/
Login: POST /auth/login/
Logout: POST /auth/logout/
Review Endpoints
List All Reviews: GET /reviews/
Create a New Review: POST /reviews/
Retrieve a Review: GET /reviews/<id>/
Update a Review: PUT /reviews/<id>/
Delete a Review: DELETE /reviews/<id>/
Filter Reviews by Movie Title or Rating: GET /reviews/?movie_title=The Lion King&rating=4

**Project Structure**
moviereviewapi/ - Django project configuration.
users/ - Handles user registration, login, and authentication.
reviews/ - Contains models, views, and serializers for managing movie reviews.
Likes/ - Contains models, views, and serializers for managing review likes.
Comments/- Contains models, views, and serializers for managing review comments.

**Models 
Review Model**
movie_title: The title of the movie being reviewed.
review_content: The content of the user's review.
rating: A rating between 1 and 5.
user: ForeignKey to the User model, representing the review's author.
created_date: Date when the review was created.

**User Model**
username: The user's unique username.
email: The user's email address.
password: The user's password

**Optional Models**
**Like Model**
user: ForeignKey to the User model, representing the user who liked the review.
review: ForeignKey to the Review model, representing the liked review.
created_date: Date when the review was liked.

**Comment Model**
review: ForeignKey to the Review model, representing the review commented on.
user: ForeignKey to the User model, representing the user who commented on the review.
content: The content of the user's comment.
created_at: Date when the review was commented on.

