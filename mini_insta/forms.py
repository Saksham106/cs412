# File: mini_insta/forms.py
# Author: Saksham Goel (saksham@bu.edu), 09/30/2025
# Description: Forms for the Mini Insta application, including post creation.

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

