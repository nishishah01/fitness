from rest_framework import serializers
from .models import userProfiles,healthData

class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfiles
        fields =['username','age','height','weight','fitnessgoals']

class healthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = healthData
        fields =['user_profile','date_recorded','weight','bmi','blood_pressure']

