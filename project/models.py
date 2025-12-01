# File: project/models.py
# Author: Saksham Goel (saksham@bu.edu), 11/23/2025
# Description: Models for the final project application.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class DiningLocation(models.Model):
    '''Model representing a dining hall or café on/near campus.'''
    name = models.CharField(max_length=200)
    location_type = models.CharField(max_length=100)
    campus_area = models.CharField(max_length=100)
    address = models.CharField(max_length=300, blank=True)
    is_on_campus = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name} ({self.location_type})'


class UserProfile(models.Model):
    '''Model representing a student who can host or join meals.'''
    DIETARY_CHOICES = [
        ('None', 'None'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Halal', 'Halal'),
        ('Kosher', 'Kosher'),
        ('Other', 'Other'),
    ]
    
    MEAL_TIME_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Late Night', 'Late Night'),
    ]
    
    VIBE_CHOICES = [
        ('Quick meal', 'Quick meal'),
        ('Study + eat', 'Study + eat'),
        ('Gym bros', 'Gym bros'),
        ('Social', 'Social'),
        ('Casual', 'Casual'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_profile')
    display_name = models.CharField(max_length=100)
    major = models.CharField(max_length=100, blank=True)
    class_year = models.IntegerField(null=True, blank=True)
    dietary_preference = models.CharField(max_length=20, choices=DIETARY_CHOICES, default='None')
    preferred_location = models.ForeignKey(DiningLocation, on_delete=models.SET_NULL, null=True, blank=True)
    usual_meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES, default='Lunch')
    vibe = models.CharField(max_length=50, choices=VIBE_CHOICES, default='Casual')
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.display_name} ({self.user.username})'


class MealPost(models.Model):
    '''Model representing a meal invitation created by a user.'''
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('full', 'Full'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    host = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey(DiningLocation, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    max_guests = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} at {self.location.name} - {self.start_time.strftime("%Y-%m-%d %H:%M")}'
    
    def get_absolute_url(self):
        return reverse('meal_detail', kwargs={'pk': self.pk})
    
    def get_accepted_guests(self):
        return JoinRequest.objects.filter(meal=self, status='accepted').count()


class JoinRequest(models.Model):
    '''Model representing a student asking to join a specific meal.'''
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('waitlisted', 'Waitlisted'),
        ('declined', 'Declined'),
    ]
    
    meal = models.ForeignKey(MealPost, on_delete=models.CASCADE)
    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.requester.display_name} -> {self.meal.title} ({self.status})'
