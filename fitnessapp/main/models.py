from django.db import models

# Create your models here.
class userProfiles(models.Model):
    username = models.CharField(max_length=255,unique=True)
    age = models.IntegerField()
    height = models.DecimalField(max_digits=6,decimal_places=2)
    weight = models.DecimalField(max_digits=6,decimal_places=2)
    fitnessgoals = models.TextField()

    def __str__(self):
        return self.username

class healthData(models.Model):
    user_profile = models.ForeignKey(userProfiles,on_delete=models.CASCADE)
    date_recorded=models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=6,decimal_places=2)  #this wiil be in kgs
    bmi= models.DecimalField(max_digits=6,decimal_places=2,blank=True, null=True)
    blood_pressure = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.user_profile.username}-{self.date_recorded}"

