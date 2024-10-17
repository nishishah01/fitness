from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import *
from django.shortcuts import get_object_or_404,redirect
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.permissions import AllowAny
import logging
logger=logging.getLogger(__name__)
class RegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset=UserProfile.objects.all()
    serializer_class=UserProfilesSerializer
    def perform_create(self, serializer):
        user=serializer.save(is_active=False)
        return user
    

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        logger.debug(f"Attempting to authenticate user: {username}")

        try:
            print(UserProfile.objects.all())
            user = UserProfile.objects.get(username=username)
            if user:
                print('User Exists')
        except UserProfile.DoesNotExist:
            logger.debug(f"User: {username} does not exist")
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):  
            if user.is_active:
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
               
                return Response({'error': 'Please verify your email to activate your account.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        return Response({
            'access': str(token.access_token),
        })

    
class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'OTP verified successfully'}, status=status.HTTP_200_OK)
    
class ResendVerificationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResendVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = UserProfile.objects.get(username=username)
            
            
            otp = get_random_string(length=6, allowed_chars='0123456789')
            user.verification_token = otp
            user.save()
            
            
            subject = "Resend OTP Verification"
            message = f"Your OTP for account verification is: {otp}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            
            send_mail(subject, message, from_email, recipient_list)
            return Response({'detail': 'OTP resent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)