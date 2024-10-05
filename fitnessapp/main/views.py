from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import userProfiles,healthData
from .serializers import UserProfilesSerializer, healthDataSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset=userProfiles.objects.all()
    serializer_class=UserProfilesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class HealthDataListCreateView(generics.ListCreateAPIView):
    queryset=healthData.objects.all()
    serializer_class=healthDataSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]