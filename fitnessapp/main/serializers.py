from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfilesSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','username','email', 'age', 'height', 'weight', 'fitness_goals', 'health_conditions','password']

    def create(self,validated_data):
        password = validated_data.pop('password')
        user= UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

class VerifyOTPSerializer(serializers.Serializer):
    username=serializers.CharField()
    otp=serializers.CharField()

    def validate(self,data):
        username=data.get('username')
        otp=data.get('otp')

        try:
            user=UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')
        
        if user.verification_token!=otp:
            raise serializers.ValidationError('invlid otp.')
        return data
    
    def save(self,**kwargs):
        username = self.validated_data['username']
        user=UserProfile.objects.get(username=username)
        user.is_active=True
        user.verification_token=''
        user.save()
        return user
    
class ResendVerificationSerializer(serializers.Serializer):
    username=serializers.CharField()

    def validate(self,data):
        username=data.get('username')


        try:
            user=UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')
        
        if user.is_active:
            raise serializers.ValidationError('user already verified')
        
        return data