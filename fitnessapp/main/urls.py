from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
   path('register/',RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/',RefreshView.as_view(), name='refresh'),

   path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
   path('resend-verification/',ResendVerificationView.as_view(), name='resend-verification'),
    path('api/user-profile/', UpdateUserProfileView.as_view(), name='update-user-profile'),
    path('fitness-plan/',FitnessPlanView.as_view(),name='fitness-plan'),
    path('fitness-plan/generate/', FitnessPlanView.as_view(), name='generate_fitness_plan'),
   
]