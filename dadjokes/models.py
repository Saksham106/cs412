# File: dadjokes/models.py
# Author: Saksham Goel (sakshamg@bu.edu), 11/11/2025
# Description: Models for the dadjokes application, including Joke and Picture.

from django.db import models
from django.urls import reverse

# Create your models here.

class Joke(models.Model):
    '''Model representing a dad joke.'''
    text = models.TextField(blank=False)
    contributor = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Joke by {self.contributor}'
    
    def get_absolute_url(self):
        return reverse('joke', kwargs={'pk': self.pk})


class Picture(models.Model):
    '''Model representing a silly picture or GIF.'''
    image_url = models.URLField(blank=False)
    contributor = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Picture by {self.contributor}'
    
    def get_absolute_url(self):
        return reverse('picture', kwargs={'pk': self.pk})
