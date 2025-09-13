# File: views.py
# Author: Saksham Goel (saksham@bu.edu), 09/12/2025
# Description: Views for the quotes Django app. Provides pages for displaying
# a random Socrates quote with an image, showing all quotes and images, and
# an about page describing the project.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

"""Views for the quotes app."""

import time
import random

QUOTES = [
    "The only true wisdom is in knowing you know nothing.",
    "The unexamined life is not worth living.",
    "The only good is knowledge, and the only evil is ignorance.",
    "Be slow to fall into friendship; but when thou art in, continue firm and constant.",
    "To find yourself, think for yourself.",
    "Let him that would move the world first move himself.",
    "I cannot teach anybody anything. I can only make them think",
    "Beware the barrenness of a busy life",
    "Strong minds discuss ideas, average minds discuss events, weak minds discuss people",
    "Education is the kindling of a flame, not the filling of a vessel",

]

IMAGES = [
    # Option 1: external URLs (easiest to start)
    "https://cdn.britannica.com/69/75569-050-7AB67C4B/herm-Socrates-half-original-Greek-Capitoline-Museums.jpg",
    "https://cdn.prod.website-files.com/65d4ce03f2c96ac479df5ad5/6673ba351148c7a07c55d28f_Socrates%2C%20resp%20to%20city%20hero.png",
    "https://media.sciencephoto.com/image/h4190520/800wm/H4190520-Socrates,_Ancient_Greek_philosopher.jpg",
    "https://www.singularityweblog.com/wp-content/uploads/2018/08/socrates-drawing.jpg",
    "https://www.meisterdrucke.us/kunstwerke/1260px/English_School_-_Portrait_of_the_Greek_philosopher_Socrates_%28469-399_BC%29_Socrates_-_-_From_series_-_%28MeisterDrucke-1061281%29.jpg",
]

def quote(request):
    context = {
        'quote': random.choice(QUOTES),
        'single_image': random.choice(IMAGES),
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {
        'quotes': QUOTES,
        'all_images': IMAGES,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    return render(request, 'quotes/about.html')
