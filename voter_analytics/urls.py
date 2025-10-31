# File: voter_analytics/urls.py
# Author: Saksham Goel (sakshamg@bu.edu), 10/27/2025
# Description: URL routes for the voter_analytics application, including voters and graphs views.

from django.urls import path
from . import views 

urlpatterns = [
	path('', views.VoterListView.as_view(), name='voters'),
	path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
	path('graphs/', views.GraphsListView.as_view(), name='graphs'),
]