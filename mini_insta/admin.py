# File: mini_insta/admin.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: Admin configuration for the Mini Insta application, registering
# the Profile model to enable management via the Django admin interface.

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)