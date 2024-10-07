from django.core.mail import EmailMessage
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from .models import userProfiles, healthData
from .serializers import UserProfilesSerializer, healthDataSerializer
from rest_framework.permissions import AllowAny
from .tokens import account_activation_token
import uuid 

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = userProfiles.objects.all()
    serializer_class = UserProfilesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class HealthDataListCreateView(generics.ListCreateAPIView):
    queryset = healthData.objects.all()
    serializer_class = healthDataSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class RegisterView(APIView):
    permission_classes=[AllowAny]
    http_method_names = ['post']
    def post(self, request):
        serializer = UserProfilesSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False 
            user.save()

            uid = user.pk 
            token =account_activation_token.make_token(user)
            mail_subject = 'Activate your account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'uid': uid,
                'token': token,
            })
            to_email = serializer.validated_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateView(APIView):
    def get(self, request, uid, token):
        try:
            user = userProfiles.objects.get(pk=uid)
        except userProfiles.DoesNotExist:
            user = None

        if user is not None and token == account_activation_token.make_token(user):
            user.is_active = True
            user.save()
            return Response({'message': 'Your account has been activated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Activation link is invalid'}, status=status.HTTP_400_BAD_REQUEST)
