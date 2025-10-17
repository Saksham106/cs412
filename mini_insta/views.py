# File: mini_insta/views.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: Class-based views for the Mini Insta application, including
# creating, updating, and deleting profiles and posts.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
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
        """Add profile to context."""
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    # Upon form submission, associate the new Post with the Profile
    def form_valid(self, form):
        """Validate the form and create a new Post and Photo objects."""
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
    
    def get_success_url(self):
        """Redirect to the newly created post's detail page."""
        pk = self.object.pk
        return reverse('show_post', kwargs={'pk': pk})

class UpdateProfileView(UpdateView):
    """Update an existing Profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    """Delete an existing Post."""
    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    
    def get_context_data(self, **kwargs):
        """Add post and profile to context."""
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['profile'] = self.get_object().profile
        return context
    
    def get_success_url(self):
        """Redirect to the profile page of the deleted post."""
        post = self.get_object()
        return reverse('show_profile', kwargs={'pk': post.profile.pk})

class UpdatePostView(UpdateView):
    """Update an existing Post."""
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class ShowFollowersDetailView(DetailView):
    """Display followers of a profile."""
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    """Display profiles that this profile is following."""
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ListView):
    """Display post feed for a profile showing posts from followed profiles."""
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        """Return posts from profiles that this profile follows."""
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        """Add profile to context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

class SearchView(ListView):
    """Search for profiles and posts based on text query."""
    template_name = 'mini_insta/search_results.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Handle GET requests - show search form if no query, otherwise show results."""
        if 'query' not in request.GET:
            # No query provided, show search form
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            return render(request, 'mini_insta/search.html', {'profile': profile})
        else:
            # Query provided, use ListView to show results
            return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return posts that match the search query."""
        query = self.request.GET.get('query', '')
        if query:
            return Post.objects.filter(caption__icontains=query).order_by('-timestamp')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        """Add profile, query, and matching profiles to context."""
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        
        # Add profile and query to context
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        context['query'] = query
        
        # Add matching profiles - search username first, then display_name, then bio_text
        if query:
            matching_profiles = []
            # Search by username
            username_matches = Profile.objects.filter(username__icontains=query)
            for profile in username_matches:
                if profile not in matching_profiles:
                    matching_profiles.append(profile)
            
            # Search by display_name
            display_name_matches = Profile.objects.filter(display_name__icontains=query)
            for profile in display_name_matches:
                if profile not in matching_profiles:
                    matching_profiles.append(profile)
            
            # Search by bio_text
            bio_matches = Profile.objects.filter(bio_text__icontains=query)
            for profile in bio_matches:
                if profile not in matching_profiles:
                    matching_profiles.append(profile)
            
            context['matching_profiles'] = matching_profiles
        else:
            context['matching_profiles'] = []
        
        return context