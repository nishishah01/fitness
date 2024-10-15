from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from django.db.models import Count

class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'age', 'height', 'weight', 'fitness_goals', 'health_conditions']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},    
            'username': {'required': True}     
        }

    def create(self, validated_data):
      
        email = validated_data.get('email')
        if not email:
            raise serializers.ValidationError({'email': 'This field is required.'})
        
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': "A user with this email already exists."})

        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password']
        )
        
        
        UserProfile.objects.create(user=user)

        return user