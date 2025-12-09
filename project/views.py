# File: project/views.py
# Author: Saksham Goel (sakshamg@bu.edu), 11/27/2025
# Description: Views for the final project application. Handles logic for meals, profiles, matching, and chat.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import MealPost, UserProfile, JoinRequest, DiningLocation, Review, MealMessage
from .forms import CreateMealPostForm, UpdateMealPostForm, CreateUserProfileForm, UpdateUserProfileForm, CreateReviewForm, MealMessageForm

# Create your views here.

class MealPostListView(ListView):
    '''Displays a list of all meal posts, with search and filtering.'''
    model = MealPost
    template_name = 'project/meal_list.html'
    context_object_name = 'meals'

    def get_queryset(self):
        '''Return a queryset of all meal posts, filtered by location, status, and date range.'''
        queryset = MealPost.objects.all()
        
        # Filter by location
        location_id = self.request.GET.get('location')
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by date range
        date_from = self.request.GET.get('date_from')
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                queryset = queryset.filter(start_time__date__gte=date_from_obj.date())
            except:
                pass
        
        date_to = self.request.GET.get('date_to')
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                queryset = queryset.filter(start_time__date__lte=date_to_obj.date())
            except:
                pass
        
        return queryset

    def get_context_data(self, **kwargs):
        '''Return the context data for the meal list view.'''
        context = super().get_context_data(**kwargs)
        context['locations'] = DiningLocation.objects.all()
        context['status_choices'] = MealPost.STATUS_CHOICES
        return context

class MealPostDetailView(DetailView):
    '''Displays details of a single meal, including join requests and chat.'''
    model = MealPost
    template_name = 'project/meal_detail.html'
    context_object_name = 'meal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal = self.get_object()
        context['join_requests'] = JoinRequest.objects.filter(meal=meal)
        
        # Check permission to chat (only host and accepted guests)
        can_chat = False
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                is_host = (meal.host == user_profile)
                is_guest = JoinRequest.objects.filter(meal=meal, requester=user_profile, status='accepted').exists()
                if is_host or is_guest:
                    can_chat = True
            except UserProfile.DoesNotExist:
                pass
        
        context['can_chat'] = can_chat
        if can_chat:
            context['chat_messages'] = meal.messages.all()
            context['chat_form'] = MealMessageForm()

        # Get list of users the current user has already reviewed for this meal
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                reviewed_user_ids = Review.objects.filter(
                    reviewer=user_profile, 
                    meal=meal
                ).values_list('reviewed_user_id', flat=True)
                context['reviewed_user_ids'] = list(reviewed_user_ids)
                
                # Check if current user has already requested
                context['has_requested'] = JoinRequest.objects.filter(meal=meal, requester=user_profile).exists()
            except UserProfile.DoesNotExist:
                context['reviewed_user_ids'] = []
                context['has_requested'] = False
        else:
            context['reviewed_user_ids'] = []
            context['has_requested'] = False
            
        return context

    def post(self, request, *args, **kwargs):
        '''Handles posting a chat message to the meal.'''
        if not request.user.is_authenticated:
            return redirect('login')
            
        self.object = self.get_object()
        meal = self.object
        
        # Verify permission
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            is_host = (meal.host == user_profile)
            is_guest = JoinRequest.objects.filter(meal=meal, requester=user_profile, status='accepted').exists()
            
            if is_host or is_guest:
                form = MealMessageForm(request.POST)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.meal = meal
                    message.sender = user_profile
                    message.save()
                    return redirect('meal_detail', pk=meal.pk)
        except UserProfile.DoesNotExist:
            pass
            
        return redirect('meal_detail', pk=meal.pk)

class CreateMealPostView(LoginRequiredMixin, CreateView):
    '''View for creating a new meal.'''
    form_class = CreateMealPostForm
    template_name = 'project/create_meal.html'

    def get_login_url(self):
        return reverse('login')

    def form_valid(self, form):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return redirect('create_profile')
        form.instance.host = user_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meal_detail', kwargs={'pk': self.object.pk})

class UpdateMealPostView(LoginRequiredMixin, UpdateView):
    '''View for updating an existing meal.'''
    model = MealPost
    form_class = UpdateMealPostForm
    template_name = 'project/update_meal.html'

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        # Only allow host to edit
        return MealPost.objects.filter(host__user=self.request.user)

    def get_success_url(self):
        return reverse('meal_detail', kwargs={'pk': self.object.pk})

class DeleteMealPostView(LoginRequiredMixin, DeleteView):
    '''View for deleting a meal.'''
    model = MealPost
    template_name = 'project/delete_meal.html'

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        '''Return a queryset of all meals hosted by the current user.'''
        return MealPost.objects.filter(host__user=self.request.user)

    def get_success_url(self):
        return reverse('meal_list')

# Authentication Views
class UserRegistrationView(CreateView):
    '''View for user registration.'''
    form_class = UserCreationForm
    template_name = 'project/register.html'
    model = User

    def get_success_url(self):
        return reverse('login')

# Profile Views
class CreateUserProfileView(LoginRequiredMixin, CreateView):
    '''View for creating a user profile.'''
    form_class = CreateUserProfileForm
    template_name = 'project/create_profile.html'

    def get_login_url(self):
        return reverse('login')

    def form_valid(self, form):
        '''Save the form and set the user profile to the current user.'''
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meal_list')

class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    '''View for updating a user profile.'''
    model = UserProfile
    form_class = UpdateUserProfileForm
    template_name = 'project/update_profile.html'

    def get_login_url(self):
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        '''Dispatch the request to the view. This is so that if the user does not have a profile, they are redirected to the create profile page.'''
        try:
            UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return redirect('create_profile')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        '''Return the context data for the update profile view.'''
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['reviews'] = Review.objects.filter(reviewed_user=user_profile).order_by('-created_at')
        context['karma'] = calculate_karma(user_profile)
        return context

    def get_success_url(self):
        return reverse('meal_list')

class UserProfileDetailView(DetailView):
    '''Public view of a user's profile.'''
    model = UserProfile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''Return the context data for the user profile detail view.'''
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['reviews'] = Review.objects.filter(reviewed_user=user_profile).order_by('-created_at')
        context['karma'] = calculate_karma(user_profile)
        return context

# JoinRequest Views
class CreateJoinRequestView(LoginRequiredMixin, CreateView):
    '''View for creating a request to join a meal.'''
    model = JoinRequest
    fields = ['message']
    template_name = 'project/create_join_request.html'

    def get_login_url(self):
        return reverse('login')

    def get_context_data(self):
        '''Return the context data for the create join request view.'''
        context = super().get_context_data()
        context['meal'] = MealPost.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        '''Save the form and set the meal and requester to the current user.'''
        meal = MealPost.objects.get(pk=self.kwargs['pk'])
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return redirect('create_profile')
        form.instance.meal = meal
        form.instance.requester = user_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meal_detail', kwargs={'pk': self.kwargs['pk']})

class UpdateJoinRequestView(LoginRequiredMixin, UpdateView):
    '''View for updating a join request.'''
    model = JoinRequest
    fields = ['message']
    template_name = 'project/update_join_request.html'

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        '''Return a queryset of all join requests for the current user.'''
        return JoinRequest.objects.filter(requester__user=self.request.user)

    def get_success_url(self):
        return reverse('meal_detail', kwargs={'pk': self.object.meal.pk})

class DeleteJoinRequestView(LoginRequiredMixin, DeleteView):
    '''View for cancelling a join request.'''
    model = JoinRequest
    template_name = 'project/delete_join_request.html'

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        '''Return a queryset of all join requests for the current user.'''
        return JoinRequest.objects.filter(requester__user=self.request.user)

    def get_success_url(self):
        return reverse('meal_detail', kwargs={'pk': self.object.meal.pk})

# Host Actions (Function-Based Views)
def accept_join_request(request, pk):
    '''Host action to accept a join request.'''
    join_request = get_object_or_404(JoinRequest, pk=pk)
    meal = join_request.meal
    
    if request.user.is_authenticated and meal.host.user == request.user:
        join_request.status = 'accepted'
        join_request.save()
        
        # If the meal is full, set the status to full
        accepted_count = meal.get_accepted_guests()
        if accepted_count >= meal.max_guests:
            meal.status = 'full'
            meal.save()
    
    return redirect('meal_detail', pk=meal.pk)

def decline_join_request(request, pk):
    '''Host action to decline a join request.'''
    join_request = get_object_or_404(JoinRequest, pk=pk)
    meal = join_request.meal
    
    if request.user.is_authenticated and meal.host.user == request.user:
        join_request.status = 'declined'
        join_request.save()
    
    return redirect('meal_detail', pk=meal.pk)

def waitlist_join_request(request, pk):
    '''Host action to waitlist a join request.'''
    join_request = get_object_or_404(JoinRequest, pk=pk)
    meal = join_request.meal
    
    if request.user.is_authenticated and meal.host.user == request.user:
        join_request.status = 'waitlisted'
        join_request.save()
    
    return redirect('meal_detail', pk=meal.pk)

# Dashboard Views
class MyHostedMealsView(LoginRequiredMixin, ListView):
    '''Displays meals hosted by the current user.'''
    model = MealPost
    template_name = 'project/my_hosted_meals.html'
    context_object_name = 'meals'

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            return MealPost.objects.filter(host=user_profile)
        except UserProfile.DoesNotExist:
            return MealPost.objects.none()

class MyJoinedMealsView(LoginRequiredMixin, ListView):
    '''Displays meals joined by the current user.'''
    model = MealPost
    template_name = 'project/my_joined_meals.html'
    context_object_name = 'meals'

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        '''Return a queryset of all meals joined by the current user.'''
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            accepted_requests = JoinRequest.objects.filter(requester=user_profile, status='accepted')
            meal_ids = accepted_requests.values_list('meal_id', flat=True)
            return MealPost.objects.filter(pk__in=meal_ids)
        except UserProfile.DoesNotExist:
            return MealPost.objects.none()

# Search & Filter View
class MealSearchView(ListView):
    '''Standalone search view (reuses meal list template).'''
    model = MealPost
    template_name = 'project/meal_list.html'
    context_object_name = 'meals'

    def get_queryset(self):
        queryset = MealPost.objects.all()
        
        # Helper logic same as MealPostListView
        location_id = self.request.GET.get('location')
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by date range from
        date_from = self.request.GET.get('date_from')
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                queryset = queryset.filter(start_time__date__gte=date_from_obj.date())
            except:
                pass
        
        # Filter by date range to
        date_to = self.request.GET.get('date_to')
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                queryset = queryset.filter(start_time__date__lte=date_to_obj.date())
            except:
                pass
        
        return queryset

    def get_context_data(self, **kwargs):
        '''Return the context data for the meal search view.'''
        context = super().get_context_data(**kwargs)
        context['locations'] = DiningLocation.objects.all()
        context['status_choices'] = MealPost.STATUS_CHOICES
        return context

# Meal Matching View
def calculate_karma(user_profile):
    '''Calculate average karma (rating) for a user.'''
    from django.db.models import Avg
    reviews = Review.objects.filter(reviewed_user=user_profile)
    if reviews.exists():
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1)
    return None

def find_meal_matches(request):
    '''Find compatible users for meal matching based on preferences.'''
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('create_profile')
    
    # Get all other user profiles
    all_profiles = UserProfile.objects.exclude(user=request.user)
    
    # Score matches based on compatibility
    matches = []
    for profile in all_profiles:
        score = 0
        match_reasons = []
        
        # Same preferred location (3 points)
        if user_profile.preferred_location and profile.preferred_location:
            if user_profile.preferred_location == profile.preferred_location:
                score += 3
                match_reasons.append(f"Same preferred location: {user_profile.preferred_location.name}")
        
        # Same meal time (2 points)
        if user_profile.usual_meal_time == profile.usual_meal_time:
            score += 2
            match_reasons.append(f"Same meal time: {user_profile.usual_meal_time}")
        
        # Compatible dietary preferences (2 points)
        if user_profile.dietary_preference == profile.dietary_preference:
            score += 2
            if user_profile.dietary_preference != 'None':
                match_reasons.append(f"Same dietary preference: {user_profile.dietary_preference}")
        
        # Same vibe (1 point)
        if user_profile.vibe == profile.vibe:
            score += 1
            match_reasons.append(f"Same vibe: {user_profile.vibe}")

        # Same social battery (2 points)
        if user_profile.social_battery == profile.social_battery:
            score += 2
            match_reasons.append(f"Same social battery: {user_profile.social_battery}")

        # Same interest (2 points)
        if user_profile.interest == profile.interest:
            score += 2
            match_reasons.append(f"Same interest: {user_profile.interest}")

        # Same spice tolerance (1 point)
        if user_profile.spice_tolerance == profile.spice_tolerance:
            score += 1
            if user_profile.spice_tolerance != 'None':
                match_reasons.append(f"Same spice tolerance: {user_profile.spice_tolerance}")
        
        # Only include profiles with at least some compatibility
        if score > 0:
            # Scale score to be out of 10 (max raw score is 13)
            scaled_score = round((score / 13) * 10, 1)
            
            # Add karma
            karma = calculate_karma(profile)
            
            matches.append({
                'profile': profile,
                'score': scaled_score,
                'karma': karma,
                'reasons': match_reasons
            })
    
    # Sort by score (highest first)
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    return render(request, 'project/meal_matches.html', {
        'matches': matches,
        'user_profile': user_profile
    })

def download_calendar_event(request, pk):
    '''Generate and download an .ics calendar file for a meal.'''
    meal = get_object_or_404(MealPost, pk=pk)
    
    # Format dates for ICS (YYYYMMDDTHHMMSSZ)
    start = meal.start_time.strftime('%Y%m%dT%H%M%S')
    
    # Default duration 1 hour if we don't have end time
    end_time = meal.start_time + timedelta(hours=1)
    end = end_time.strftime('%Y%m%dT%H%M%S')
    
    # Construct ICS content
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Campus Meal Matching//EN",
        "BEGIN:VEVENT",
        f"SUMMARY:{meal.title}",
        f"DTSTART:{start}",
        f"DTEND:{end}",
        f"DESCRIPTION:Host: {meal.host.display_name}\\n{meal.description}",
        f"LOCATION:{meal.location.name}",
        "END:VEVENT",
        "END:VCALENDAR"
    ]
    
    # Generate the ICS content and return the response
    response = HttpResponse('\n'.join(ics_content), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="meal_{pk}.ics"'
    return response

def add_review(request, pk):
    '''Add a review for a user after a meal.'''
    if not request.user.is_authenticated:
        return redirect('login')
    
    reviewed_user = get_object_or_404(UserProfile, pk=pk)
    meal_id = request.GET.get('meal')
    meal = get_object_or_404(MealPost, pk=meal_id)
    
    # Check if review already exists
    try:
        reviewer_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('create_profile')

    existing_review = Review.objects.filter(reviewer=reviewer_profile, reviewed_user=reviewed_user, meal=meal).exists()
    
    if existing_review:
        # Redirect or show error if already reviewed
        return redirect('meal_detail', pk=meal.pk)

    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = reviewer_profile
            review.reviewed_user = reviewed_user
            review.meal = meal
            review.save()
            return redirect('meal_detail', pk=meal.pk)
    else:
        form = CreateReviewForm()
    
    return render(request, 'project/add_review.html', {
        'form': form,
        'reviewed_user': reviewed_user,
        'meal': meal
    })