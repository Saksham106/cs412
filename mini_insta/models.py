from django.db import models

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
    
