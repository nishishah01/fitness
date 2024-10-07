from rest_framework import serializers
from .models import userProfiles,healthData

class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfiles
        fields =['username','age','height','weight','fitnessgoals']

    def create(self,validated_data):
        user=userProfiles.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class healthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = healthData
        fields =['user_profile','date_recorded','weight','bmi','blood_pressure']
