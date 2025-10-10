# File: mini_insta/urls.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: URL routes for the Mini Insta application, including profile,
# post, and photo views.

from django.urls import path
from .views import *

# Purpose: Define app URL patterns used by the project-level router.
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post')
]
