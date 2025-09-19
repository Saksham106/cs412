# File: restaurant/urls.py
# Author: Saksham Goel (sakshamg@bu.edu), 09/14/2025
# Description: URL configuration for restaurant app

from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    path(r'main/', views.main, name='main'),
    path(r'order/', views.order, name='order'),
    path(r'confirmation/', views.confirmation, name='confirmation'),
]
