from django.contrib.auth.backends import BaseBackend
from .models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class CustomAuthBackend(BaseBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.email:
                if check_password(password, user.password) :
                    date_time=timezone.now()
                    user.last_login=date_time
                    user.save()
                     # Issue JWT tokens
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    # Return the user and JWT tokens
                    return {
                        'user_object': user,
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'success':"User Found"
                    }
                else:
                    return {'error':'Password is Wrong !!'}
            else:
                return {'error':"Email Id is not registered with us..."}
        except User.DoesNotExist:
            return {'error':"Email is not registered with us.."}
    
 
