# File: mini_insta/views.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: Class-based views for the Mini Insta application, including
# creating, updating, and deleting profiles and posts.

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import *
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
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

class MyProfileView(LoginRequiredMixin, DetailView):
    """Display the logged-in user's profile."""
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        """Return the profile for the logged-in user."""
        return Profile.objects.get(user=self.request.user)

class PostDetailView(DetailView):
    """Display a single Post selected by its primary key."""
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new Post for a given Profile."""
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        """Return the profile for the logged-in user."""
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self):
        """Add profile to context."""
        context = super().get_context_data()
        context['profile'] = self.get_object()
        return context

    # Upon form submission, associate the new Post with the Profile
    def form_valid(self, form):
        """Validate the form and create a new Post and Photo objects."""
        profile = self.get_object()
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

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update an existing Profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        """Return the profile for the logged-in user."""
        return Profile.objects.get(user=self.request.user)

class DeletePostView(LoginRequiredMixin, DeleteView):
    """Delete an existing Post."""
    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
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

class UpdatePostView(LoginRequiredMixin, UpdateView):
    """Update an existing Post."""
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

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

class PostFeedListView(LoginRequiredMixin, ListView):
    """Display post feed for a profile showing posts from followed profiles."""
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        """Return the profile for the logged-in user."""
        return Profile.objects.get(user=self.request.user)
    
    def get_queryset(self):
        """Return posts from profiles that this profile follows."""
        profile = self.get_object()
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        """Add profile to context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

class SearchView(LoginRequiredMixin, ListView):
    """Search for profiles and posts based on text query."""
    template_name = 'mini_insta/search_results.html'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        """Return the profile for the logged-in user."""
        return Profile.objects.get(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        """Handle GET requests - show search form if no query, otherwise show results."""
        if 'query' not in request.GET:
            # No query provided, show search form
            profile = self.get_object()
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
        context['profile'] = self.get_object()
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


class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''
    template_name = 'mini_insta/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')


class CreateProfileView(CreateView):
    """Create a new Profile with associated User account."""
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'
    
    def get_context_data(self, **kwargs):
        """Add UserCreationForm to context."""
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        context['profile_form'] = self.get_form()
        return context
    
    def form_valid(self, form):
        """Handle both User and Profile creation."""
        # Create the User first
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            
            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Attach the User to the Profile
            form.instance.user = user
            
            # Save the Profile
            response = super().form_valid(form)
            
            # Redirect to the new profile
            return response
        else:
            # If user form is invalid, return to form with errors
            return self.form_invalid(form)
    
    def get_success_url(self):
        """Redirect to the newly created profile."""
        return reverse('my_profile')


class FollowProfileView(LoginRequiredMixin, TemplateView):
    """Follow a profile."""
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        """Handle the follow operation."""
        if request.method == 'POST':
            # Get the profile to follow
            profile_to_follow = get_object_or_404(Profile, pk=kwargs['pk'])
            
            # Get the current user's profile
            current_profile = Profile.objects.get(user=request.user)
            
            # Don't allow following yourself
            if current_profile != profile_to_follow:
                # Create the follow relationship
                Follow.objects.get_or_create(
                    follower=current_profile,
                    following=profile_to_follow
                )
            
            # Redirect back to the profile page
            return redirect('show_profile', pk=profile_to_follow.pk)
        
        return super().dispatch(request, *args, **kwargs)


class UnfollowProfileView(LoginRequiredMixin, TemplateView):
    """Unfollow a profile."""
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        """Handle the unfollow operation."""
        if request.method == 'POST':
            # Get the profile to unfollow
            profile_to_unfollow = get_object_or_404(Profile, pk=kwargs['pk'])
            
            # Get the current user's profile
            current_profile = Profile.objects.get(user=request.user)
            
            # Delete the follow relationship if it exists
            Follow.objects.filter(
                follower=current_profile,
                following=profile_to_unfollow
            ).delete()
            
            # Redirect back to the profile page
            return redirect('show_profile', pk=profile_to_unfollow.pk)
        
        return super().dispatch(request, *args, **kwargs)


class LikePostView(LoginRequiredMixin, TemplateView):
    """Like a post."""
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        """Handle the like operation."""
        if request.method == 'POST':
            # Get the post to like
            post_to_like = get_object_or_404(Post, pk=kwargs['pk'])
            
            # Get the current user's profile
            current_profile = Profile.objects.get(user=request.user)
            
            # Don't allow liking your own post
            if current_profile != post_to_like.profile:
                # Create the like relationship
                Like.objects.get_or_create(
                    profile=current_profile,
                    post=post_to_like
                )
            
            # Redirect back to the post page
            return redirect('show_post', pk=post_to_like.pk)
        
        return super().dispatch(request, *args, **kwargs)


class UnlikePostView(LoginRequiredMixin, TemplateView):
    """Unlike a post."""
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        """Handle the unlike operation."""
        if request.method == 'POST':
            # Get the post to unlike
            post_to_unlike = get_object_or_404(Post, pk=kwargs['pk'])
            
            # Get the current user's profile
            current_profile = Profile.objects.get(user=request.user)
            
            # Delete the like relationship if it exists
            Like.objects.filter(
                profile=current_profile,
                post=post_to_unlike
            ).delete()
            
            # Redirect back to the post page
            return redirect('show_post', pk=post_to_unlike.pk)
        
        return super().dispatch(request, *args, **kwargs)