from django.urls import path
from .views import *

urlpatterns = [
    path('', MealPostListView.as_view(), name='meal_list'),
    path('meal/<int:pk>', MealPostDetailView.as_view(), name='meal_detail'),
]
