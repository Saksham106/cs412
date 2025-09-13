# File: urls.py
# Author: Saksham Goel (saksham@bu.edu), 09/09/2025
# Description: URL configuration for the "quotes" Django app. Routes the
# main random-quote page, the show-all page, and the about page.

"""URL patterns for the quotes app."""

from django.urls import path
from . import views

# Each path maps a URL pattern (relative to where this app is included)
# to a view function in views.py.
urlpatterns = [
    path("", views.quote, name="quote"),            # /quotes/ → random quote + image
    path("quote/", views.quote, name="quote"),      # /quotes/quote/ → same as main
    path("show_all/", views.show_all, name="show_all"),  # /quotes/show_all/ → list all
    path("about/", views.about, name="about"),           # /quotes/about/ → about page
]
