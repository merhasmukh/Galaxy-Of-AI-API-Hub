# chat/urls.py
from django.urls import path
from . import views
from .views import CustomTokenObtainPairView,GoogleAuthAPIView,TokenValidation
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('user_register/', views.user_register_data, name='user_register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_login/', views.user_login_data, name='user_login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verify_reset_token/', views.verify_reset_token, name='verify_reset_token'),
    path('reset_password_confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    path('user_details/<int:user_id>/', views.get_user_details, name='user-details'),
    path("google/", GoogleAuthAPIView.as_view(), name="google-auth"),
    path('validate_token/', TokenValidation.as_view(), name='validate-token')



]
