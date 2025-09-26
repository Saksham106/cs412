# File: mini_insta/urls.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: URL routes for the Mini Insta application, mapping list and
# detail views for Profile records.

from django.urls import path
from .views import ProfileListView, ProfileDetailView

# Purpose: Define app URL patterns used by the project-level router.
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
]
