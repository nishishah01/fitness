from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .models import UserProfile
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
import os,requests
import logging
logger=logging.getLogger(__name__)
class RegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset=UserProfile.objects.all()
    serializer_class=UserProfilesSerializer
    def perform_create(self, serializer):
        user=serializer.save(is_active=False)
        return user
class UpdateUserProfileView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated] 
    serializer_class = UserProfilesSerializer

    def get_object(self):
       
        return self.request.user

    def patch(self, request, *args, **kwargs):
        logger.info(f"Request data: {request.data}") 
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)  # partial=True allows for PATCH request
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    

class FitnessPlanView(APIView):
    permission_classes = [IsAuthenticated]  #only logged in users access kar sakte hai

    def post(self, request):
        user_data = {
            "age": request.user.age,
            "weight": request.user.weight,
            "height": request.user.height,
            "fitness_goals": request.user.fitness_goals,
            "health_conditions": request.user.health_conditions,
        }
        
        prompt = (
    f"Create a detailed weekly workout and nutrition plan for a user with the following characteristics:\n"
    f"- Age: {user_data['age']}\n"
    f"- Weight: {user_data['weight']} kg\n"
    f"- Height: {user_data['height']} cm\n"
    f"- Fitness Goals: {user_data['fitness_goals']}\n"
    f"- Health Conditions: {user_data['health_conditions']}\n\n"
    "The plan should cover the following details in a clear, sectioned format:\n\n"
    "Please format the response as follows without using special symbols for line breaks or emphasis:\n\n"
    "## Weekly Workout Plan:\n"
    "- Provide a breakdown for each day of the week, including warm-up, workout exercises (with sets and reps), and cool-down activities.\n"
    "- Specify rest or active recovery days where applicable.\n\n"
    "## Weekly Nutrition Plan:\n"
    "- Include daily meal suggestions (breakfast, lunch, dinner, and snacks) focusing on whole foods, lean proteins, healthy fats, and complex carbohydrates.\n"
    "- Mention hydration tips and any specific dietary recommendations.\n\n"
    "## Tips for Success:\n"
    "- Provide actionable advice on staying consistent, tracking progress, and adjusting the plan if needed.\n"
    "- Emphasize the importance of consulting healthcare professionals if necessary.\n\n"
    "Please format the plan in a clean, bulleted format with headers for each section to make it easy to read."
)

        # URL, headers, and params setup
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": settings.GENAI_API_KEY
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # Sending the request
        try:
            response = requests.post(url, headers=headers, params=params, json=data)
            if response.status_code == 200:
                # Check if response has content before attempting to parse
                if response.text:
                    plan = response.json()
                    return Response({"message":"Workout Plan generated Successfullly","plan":{response.text}}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Empty response from the server"}, status=status.HTTP_204_NO_CONTENT)
            else:
                # Log details for failed request
                return Response(
                    {"error": "Failed to create a plan", "status_code": response.status_code, "details": response.text}, 
                    status=response.status_code
                )
        except requests.exceptions.RequestException as e:
            return Response({"error": f"RequestException: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"error": f"ValueError in JSON parsing: {str(ve)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)