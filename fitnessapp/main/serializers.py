from rest_framework import serializers
from .models import UserProfile,FitnessPlan
from django.contrib.auth.models import User


class UserProfilesSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # write_only and optional
    username = serializers.CharField(write_only=True)  # username is write-only
    email = serializers.EmailField(write_only=True)    # email is write only

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'age', 'height', 'weight', 'fitness_goals', 'health_conditions', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserProfile(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Password, username, and email shouldn't be updated here
        validated_data.pop('username', None)
        validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance
    

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
    

class FitnessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessPlan
        fields = '__all__' 
        read_only_fields = ['user', 'created_at']