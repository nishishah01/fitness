from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
urlpatterns=[
    path('profiles/',UserProfileListCreateView.as_view(),name='profile-list-create'),
    path('health-data/',HealthDataListCreateView.as_view(),name='health-data-list'),

    path('token/', TokenObtainPairView.as_view(), name='obtain-details'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
     path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('activate/<uidb64>/<token>/',ActivateView.as_view(), name='activate'),

]