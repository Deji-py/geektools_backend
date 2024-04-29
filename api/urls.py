from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('register/', views.registerUsers, name='register'),
    path('change-password/', views.changePasswordView, name='change-password'),
    path('verify_code/', views.code_verification, name='verify_code'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
]