from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']
    
    image_url = forms.URLField(label="Image URL", required=False)

