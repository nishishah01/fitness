from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models

class UserProfile(AbstractUser):
    
    age=models.IntegerField(null=True)
    weight=models.FloatField(null=False, default=0.0)
    height=models.FloatField(null=False, default=0.0)
    fitness_goals=models.TextField(null=True,blank=True)
    health_conditions=models.TextField(blank=True,null=True)
    email = models.EmailField(('email address'), unique=True)
    verification_token=models.CharField(max_length=50,null=True,blank=True)


    def get_object(self):
        return self.request.user