# File: project/urls.py
# Author: Saksham Goel (sakshamg@bu.edu), 11/25/2025
# Description: URL patterns for the final project application.

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # Meal related URLs
    path('', MealPostListView.as_view(), name='meal_list'),
    path('search', MealSearchView.as_view(), name='meal_search'),
    path('meal/<int:pk>', MealPostDetailView.as_view(), name='meal_detail'),
    path('meal/create', CreateMealPostView.as_view(), name='create_meal'),
    path('meal/<int:pk>/update', UpdateMealPostView.as_view(), name='update_meal'),
    path('meal/<int:pk>/delete', DeleteMealPostView.as_view(), name='delete_meal'),
    
    # Join Request URLs
    path('meal/<int:pk>/join', CreateJoinRequestView.as_view(), name='create_join_request'),
    path('join_request/<int:pk>/update', UpdateJoinRequestView.as_view(), name='update_join_request'),
    path('join_request/<int:pk>/delete', DeleteJoinRequestView.as_view(), name='delete_join_request'),
    path('join_request/<int:pk>/accept', accept_join_request, name='accept_join_request'),
    path('join_request/<int:pk>/decline', decline_join_request, name='decline_join_request'),
    path('join_request/<int:pk>/waitlist', waitlist_join_request, name='waitlist_join_request'),
    
    # User Dashboard URLs
    path('my_hosted_meals', MyHostedMealsView.as_view(), name='my_hosted_meals'),
    path('my_joined_meals', MyJoinedMealsView.as_view(), name='my_joined_meals'),
    
    # Matching and Features
    path('find_matches', find_meal_matches, name='find_matches'),
    path('meal/<int:pk>/calendar', download_calendar_event, name='download_calendar'),
    path('review/<int:pk>/add', add_review, name='add_review'),
    
    # Authentication & Profile
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='meal_list'), name='logout'),
    path('profile/create', CreateUserProfileView.as_view(), name='create_profile'),
    path('profile/update', UpdateUserProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail'),
]
