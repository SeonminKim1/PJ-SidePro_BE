from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user import views


urlpatterns = [
    path('', views.UserAPIView.as_view(), name="user_view"),
    path('join/', views.JoinView.as_view(), name="join_view"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')    
]