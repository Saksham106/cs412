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
    
    def get_followers(self):
        """Return a list of profiles that follow this profile."""
        return Profile.objects.filter(follower_profile__profile=self)
    
    def get_num_followers(self):
        """Return the count of followers."""
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        """Return a list of profiles that this profile follows."""
        return Profile.objects.filter(profile__follower_profile=self)
    
    def get_num_following(self):
        """Return the count of profiles being followed."""
        return Follow.objects.filter(follower_profile=self).count()

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
    
    def get_all_comments(self):
        """Return all comments on this post."""
        return Comment.objects.filter(post=self).order_by('-timestamp')
    
    def get_likes(self):
        """Return all likes on this post."""
        return Like.objects.filter(post=self)
    
    def get_num_likes(self):
        """Return the count of likes on this post."""
        return Like.objects.filter(post=self).count()

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

class Follow(models.Model):
    '''Model representing a follow relationship between two profiles.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'

class Comment(models.Model):
    '''Model representing a comment on a post.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f'{self.text}'

class Like(models.Model):
    '''Model representing a like on a post.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile.display_name} likes post by {self.post.profile.display_name}'
    