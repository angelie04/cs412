# dadjokes/urls.py
# defines URL patterns for the dadjokes app
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='dadjokes'),
    path('random/', index, name='dadjokes_random'),
    path('jokes/', JokeListView.as_view(), name = 'joke_list'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name = 'joke_detail'),
    path('picutres/', PictureListView.as_view(), name = 'pictures_list'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name = 'picture_detail'),
    
    # API URLs
    path('api/', RandomJokeAPIView.as_view(), name='api_joke'),
    path('api/random/', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random_picture/', RandomPictureAPIView.as_view(), name='api_random_picture'),
    path('api/jokes/', JokesListAPIView.as_view(), name='api_joke_list'),
    path('api/joke/<int:pk>/', JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures/', PicturesListAPIView.as_view(), name='api_picture_list'),
    path('api/picture/<int:pk>/', PictureDetailAPIView.as_view(), name='api_picture_detail'),

]