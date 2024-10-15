from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.IntegerField()
    weight=models.FloatField()
    height=models.FloatField()
    fitness_goals=models.TextField()
    health_conditions=models.TextField(blank=True,null=True)
    email = models.EmailField(('email address'), unique=True)


    def __str__(self):
        return self.user.username