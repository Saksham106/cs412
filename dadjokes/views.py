from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
import random
from rest_framework import generics
from .serializers import *


# Create your views here.

class RandomJokeAndPictureView(TemplateView):
    '''View to show one random joke and one random picture.'''
    template_name = 'dadjokes/random.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jokes = list(Joke.objects.all())
        pictures = list(Picture.objects.all())
        if jokes:
            context['joke'] = random.choice(jokes)
        if pictures:
            context['picture'] = random.choice(pictures)
        return context


class JokeListView(ListView):
    '''View to show all jokes.'''
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'


class JokeDetailView(DetailView):
    '''View to show one joke by primary key.'''
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'


class PictureListView(ListView):
    '''View to show all pictures.'''
    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'


class PictureDetailView(DetailView):
    '''View to show one picture by primary key.'''
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'


# REST API Views

class RandomJokeAPIView(generics.RetrieveAPIView):
    '''API view to return one random joke.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
    
    def get_object(self):
        jokes = list(Joke.objects.all())
        if jokes:
            return random.choice(jokes)
        return None


class JokeListAPIView(generics.ListCreateAPIView):
    '''API view to return all jokes and create a new joke.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    '''API view to return one joke by primary key.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    '''API view to return all pictures.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    '''API view to return one picture by primary key.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(generics.RetrieveAPIView):
    '''API view to return one random picture.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    
    def get_object(self):
        pictures = list(Picture.objects.all())
        if pictures:
            return random.choice(pictures)
        return None
