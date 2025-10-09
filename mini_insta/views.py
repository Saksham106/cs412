# File: mini_insta/views.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: Class-based views for the Mini Insta application, including
# listing profiles, displaying profile and post details, and creating posts.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import CreatePostForm
from django.urls import reverse


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

class PostDetailView(DetailView):
    """Display a single Post selected by its primary key."""
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    """Create a new Post for a given Profile."""
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    # Upon form submission, associate the new Post with the Profile
    def form_valid(self, form):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        
        # Save the post first
        response = super().form_valid(form)
        
        # Create Photo objects for any uploaded files (input name: 'files')
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(
                post=self.object,
                image_file=file
            )
        
        return response