from django.urls import path
from .views import UserProfileListCreateView,HealthDataListCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns=[
    path('profiles/',UserProfileListCreateView.as_view(),name='profile-list-create'),
    path('health-data/',HealthDataListCreateView.as_view(),name='health-data-list'),

    path('token/', TokenObtainPairView.as_view(), name='obtain-details'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh')
]