# File: project/models.py
# Author: Saksham Goel (sakshamg@bu.edu), 11/25/2025
# Description: Database models for the meal matching application, including UserProfile, MealPost, and Reviews.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class DiningLocation(models.Model):
    '''Represents a dining location on campus.'''
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    capacity = models.IntegerField(default=100)
    location_type = models.CharField(max_length=50) # 'Dining Hall', 'Cafe', 'Restaurant'
    
    def __str__(self):
        return f"{self.name} ({self.location_type})"

class UserProfile(models.Model):
    '''Extended user profile with preferences for meal matching.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_profile')
    display_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    
    # Preference Fields
    DIETARY_CHOICES = [
        ('None', 'I eat everything 😋'),
        ('Vegetarian', 'Vegetarian 🥗'),
        ('Vegan', 'Vegan 🌱'),
        ('Halal', 'Halal 🥩'),
        ('Kosher', 'Kosher 🕍'),
        ('Gluten-Free', 'Gluten-Free 🌾'),
        ('Nut-Free', 'Nut-Free 🥜'),
    ]
    dietary_preference = models.CharField(max_length=20, choices=DIETARY_CHOICES, default='None')
    
    preferred_location = models.ForeignKey(DiningLocation, on_delete=models.SET_NULL, null=True, blank=True)
    
    MEAL_TIME_CHOICES = [
        ('Breakfast', 'Breakfast (7am-10am) 🍳'),
        ('Lunch', 'Lunch (11am-2pm) 🥪'),
        ('Dinner', 'Dinner (5pm-8pm) 🍝'),
        ('Late Night', 'Late Night (9pm-12am) 🌙'),
    ]
    usual_meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES, default='Lunch')

    VIBE_CHOICES = [
        ('Chatty', 'Chatty & Social 🗣️'),
        ('Quiet', 'Quiet & Chill 🤫'),
        ('Quick', 'Quick Eat 🏃'),
        ('Study', 'Study & Eat 📚'),
    ]
    vibe = models.CharField(max_length=20, choices=VIBE_CHOICES, default='Chatty')

    SOCIAL_BATTERY_CHOICES = [
        ('Low', 'Low 🪫'),
        ('Medium', 'Medium 🔋'),
        ('High', 'High ⚡'),
        ('Casual', 'Casual Chat 💬'),
    ]
    social_battery = models.CharField(max_length=20, choices=SOCIAL_BATTERY_CHOICES, default='Medium')

    INTEREST_CHOICES = [
        ('Sports', 'Sports 🏀'),
        ('Tech', 'Tech & Coding 💻'),
        ('Arts', 'Arts & Music 🎨'),
        ('Gaming', 'Gaming 🎮'),
        ('Outdoors', 'Outdoors 🌲'),
        ('Movies', 'Movies & TV 🎬'),
    ]
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES, default='Tech')

    SPICE_TOLERANCE_CHOICES = [
        ('None', 'None 🥛'),
        ('Mild', 'Mild 🌶️'),
        ('Medium', 'Medium 🌶️🌶️'),
        ('Hot', 'Hot 🌶️🌶️🌶️'),
        ('Extreme', 'Extreme 🔥'),
    ]
    spice_tolerance = models.CharField(max_length=20, choices=SPICE_TOLERANCE_CHOICES, default='Medium')
    
    major = models.CharField(max_length=100, blank=True)
    class_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.display_name

class MealPost(models.Model):
    '''Represents a meal event hosted by a user.'''
    host = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='hosted_meals')
    title = models.CharField(max_length=100)
    location = models.ForeignKey(DiningLocation, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    description = models.TextField(blank=True)
    max_guests = models.IntegerField(default=1)
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('full', 'Full'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.location.name}"

    def get_absolute_url(self):
        return reverse('meal_detail', kwargs={'pk': self.pk})

    def get_accepted_guests(self):
        '''Return the number of accepted guests for this meal.'''
        return self.joinrequest_set.filter(status='accepted').count()

class JoinRequest(models.Model):
    '''Represents a request from a user to join a meal.'''
    meal = models.ForeignKey(MealPost, on_delete=models.CASCADE)
    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('waitlisted', 'Waitlisted'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.display_name} -> {self.meal.title}"

class Review(models.Model):
    '''Represents a review given by one user to another after a meal.'''
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_received')
    meal = models.ForeignKey(MealPost, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # A user can only review another user once per meal
        unique_together = ('reviewer', 'reviewed_user', 'meal')
    
    def __str__(self):
        return f'{self.reviewer.display_name} -> {self.reviewed_user.display_name} ({self.rating}*)'

class MealMessage(models.Model):
    '''Represents a chat message within a meal group.'''
    meal = models.ForeignKey(MealPost, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.display_name}: {self.message[:20]}"
