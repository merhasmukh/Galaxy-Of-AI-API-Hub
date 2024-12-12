from django.urls import path
from .views import UserSignupView, UserLoginView,ProtectedView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('protected/', ProtectedView.as_view(), name='protected-view'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint

]
