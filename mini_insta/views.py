# File: mini_insta/views.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: Class-based views for listing all profiles and showing a single
# profile.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile


class ProfileListView(ListView):
    """List all Profile records for display on the index page."""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    """Display a single Profile selected by its primary key."""
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
