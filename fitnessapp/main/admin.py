from django.contrib import admin
from .models import UserProfile
# Register your models here.
from django.contrib.auth.models import User
admin.site.register(UserProfile)