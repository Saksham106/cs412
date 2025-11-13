from django.urls import path
from .views import *

urlpatterns = [
    # Web URLs
    path('', RandomJokeAndPictureView.as_view(), name='random'),
    path('random', RandomJokeAndPictureView.as_view(), name='random'),
    path('jokes', JokeListView.as_view(), name='jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='joke'),
    path('pictures', PictureListView.as_view(), name='pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='picture'),
    
    # REST API URLs
    path('api/', RandomJokeAPIView.as_view()),
    path('api/random', RandomJokeAPIView.as_view()),
    path('api/jokes', JokeListAPIView.as_view()),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view()),
    path('api/pictures', PictureListAPIView.as_view()),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view()),
    path('api/random_picture', RandomPictureAPIView.as_view()),
]

