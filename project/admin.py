# File: project/admin.py
# Author: Saksham Goel (sakshamg@bu.edu), 11/26/2025
# Description: Register models for the admin interface.

from django.contrib import admin
from .models import DiningLocation, UserProfile, MealPost, JoinRequest, Review, MealMessage

# Register your models here.
admin.site.register(DiningLocation)
admin.site.register(UserProfile)
admin.site.register(MealPost)
admin.site.register(JoinRequest)
admin.site.register(Review)
admin.site.register(MealMessage)
