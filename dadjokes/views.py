from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Joke, Picture
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    """Followed similar layout to previous assigment views.py files.
    Showes one random Joke and one random Picture."""
    joke = Joke.objects.order_by('?').first()   
    picture = Picture.objects.order_by('?').first()
    return render(request, "dadjokes/index.html", {"joke": joke, "picture": picture})

class JokeListView(ListView):
    """View to display list of Jokes"""
    model = Joke
    template_name = "dadjokes/jokes.html"
    context_object_name = "jokes"

class JokeDetailView(DetailView):
    """View to display a single Joke"""
    model = Joke
    template_name = "dadjokes/joke_detail.html"
    context_object_name = "joke"

class PictureListView(ListView):
    """View to display list of Pictures"""
    model = Picture
    template_name = "dadjokes/pictures.html"
    context_object_name = "pictures"

class PictureDetailView(DetailView):
    """View to display a single Picture"""
    model = Picture
    template_name = "dadjokes/picture_detail.html"
    context_object_name = "picture"

# REST API:
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

class RandomJokeAPIView(APIView):
    """API view that returns a Json representation of one joke at random"""
    def get(self, request, format=None):
        joke = Joke.objects.order_by('?').first()
        if not joke:
            return Response({"detail": "No jokes found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)

class RandomPictureAPIView(APIView):
    """API view that returns a Json representation of one picture at random"""
    def get(self, request, format=None):
        picture = Picture.objects.order_by('?').first()
        if not picture:
            return Response({"detail": "No pictures found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
    
class JokesListAPIView(generics.ListCreateAPIView):
    """API view that returns a list of all jokes"""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    """API view that returns one joke by its primary key"""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
    
class PicturesListAPIView(generics.ListAPIView):
    """API view that returns a list of all pictures"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    """API view that returns one picture by its primary key"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer