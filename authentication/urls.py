from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import user_registration_data


urlpatterns = [
    path('user_registration/', user_registration_data, name='user_registration'),

    # path('login/', UserLoginView.as_view(), name='user-login'),
    # path('protected/', ProtectedView.as_view(), name='protected-view'),
    # path('users/', UserListView.as_view(), name='user-list'),

]
