from django.contrib import admin

# Register your models here.
from .models import DiningLocation, UserProfile, MealPost, JoinRequest

admin.site.register(DiningLocation)
admin.site.register(UserProfile)
admin.site.register(MealPost)
admin.site.register(JoinRequest)
