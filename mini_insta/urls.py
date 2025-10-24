# File: mini_insta/urls.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: URL routes for the Mini Insta application, including profile,
# post, and photo views.

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

# Purpose: Define app URL patterns used by the project-level router.
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/like', LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/delete_like', UnlikePostView.as_view(), name='unlike_post'),
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/follow', FollowProfileView.as_view(), name='follow_profile'),
    path('profile/<int:pk>/delete_follow', UnfollowProfileView.as_view(), name='unfollow_profile'),
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', SearchView.as_view(), name='search'),
    path('profile/', MyProfileView.as_view(), name='my_profile'),
    
    # authentication views
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]
