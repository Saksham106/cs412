from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import MealPost

# Create your views here.

class MealPostListView(ListView):
    model = MealPost
    template_name = 'project/meal_list.html'
    context_object_name = 'meals'

class MealPostDetailView(DetailView):
    model = MealPost
    template_name = 'project/meal_detail.html'
    context_object_name = 'meal'
