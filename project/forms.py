# File: project/forms.py
# Author: Saksham Goel (sakshamg@bu.edu), 11/27/2025
# Description: Forms for creating and updating meals, user profiles, reviews, and chat.

from django import forms
from .models import MealPost, UserProfile, Review, MealMessage

class CreateMealPostForm(forms.ModelForm):
    '''Form for creating a new meal.'''
    class Meta:
        model = MealPost
        fields = ['title', 'description', 'location', 'start_time', 'max_guests', 'status']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class UpdateMealPostForm(forms.ModelForm):
    '''Form for updating a meal.'''
    class Meta:
        model = MealPost
        fields = ['title', 'description', 'location', 'start_time', 'max_guests', 'status']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CreateUserProfileForm(forms.ModelForm):
    '''Form for creating a user profile.'''
    class Meta:
        model = UserProfile
        fields = ['display_name', 'major', 'class_year', 'dietary_preference', 'preferred_location', 'usual_meal_time', 'vibe', 'social_battery', 'interest', 'spice_tolerance', 'bio']

class UpdateUserProfileForm(forms.ModelForm):
    '''Form for updating a user profile.'''
    class Meta:
        model = UserProfile
        fields = ['display_name', 'major', 'class_year', 'dietary_preference', 'preferred_location', 'usual_meal_time', 'vibe', 'social_battery', 'interest', 'spice_tolerance', 'bio']

class CreateReviewForm(forms.ModelForm):
    '''Form for submitting a review.'''
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'rating-select'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'How was your meal with this person?'}),
        }

class MealMessageForm(forms.ModelForm):
    '''Form for sending a chat message.'''
    class Meta:
        model = MealMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'placeholder': 'Type a message...', 'class': 'chat-input', 'autocomplete': 'off'}),
        }
        labels = {
            'message': ''
        }
