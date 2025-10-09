# File: mini_insta/models.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: Models for the Mini Insta application, including Profile, Post, and Photo. 

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Model representing a user profile.'''
    username = models.CharField(max_length=150, blank=False)
    display_name = models.CharField(max_length=150, blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile: {self.username}'
    
    def get_all_posts(self):
        return Post.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class Post(models.Model):
    '''Model representing a post made by a user.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f'Post by {self.profile.username} | caption: {self.caption[:15]}...'
    
    def get_all_photos(self):
        return Photo.objects.filter(post=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_post', kwargs={'pk': self.pk})

class Photo(models.Model):
    '''Model representing a photo associated with a post.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.image_url:
            return f'Photo (url) for post {self.post.caption[:15]}...'
        if self.image_file:
            return f'Photo (file:{self.image_file.name}) for post {self.post.caption[:15]}...'
        return f'Photo for post {self.post.caption[:15]}...'
    
    def get_image_url(self):
        """Return the best URL for this photo: prefer image_url, else image_file.url."""
        if self.image_url:
            return self.image_url
        if self.image_file:
            try:
                return self.image_file.url
            except ValueError:
                return ''
        return ''
    