from django.contrib.auth.models import AbstractUser

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
    
class FitnessPlan(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="fitness_plans")
    created_at = models.DateTimeField(auto_now_add=True)

    
    day1_workout = models.TextField()
    day1_diet = models.TextField()
    day2_workout = models.TextField()
    day2_diet = models.TextField()
    day3_workout = models.TextField()
    day3_diet = models.TextField()
    day4_workout = models.TextField()
    day4_diet = models.TextField()
    day5_workout = models.TextField()
    day5_diet = models.TextField()
    day6_workout = models.TextField()
    day6_diet = models.TextField()
    day7_workout = models.TextField()
    day7_diet = models.TextField()

    def __str__(self):
        return f"Fitness Plan for {self.user.username} - {self.created_at}"