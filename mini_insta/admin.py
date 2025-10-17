# File: mini_insta/admin.py
# Author: Saksham Goel (saksham@bu.edu), 09/24/2025
# Description: Admin configuration for the Mini Insta application, registering
# the Profile, Post, and Photo models.

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo, Follow, Comment, Like
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
