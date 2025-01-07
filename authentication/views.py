from functools import wraps
import logging
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
from .serializers import UserRegistrationSerializer

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    methods=['post'],
    operation_description="This endpoint allows users to register.",
    request_body=UserRegistrationSerializer,  # Specify the input schema
    responses={
        201: openapi.Response("Registration successful!"),
        400: openapi.Response("Invalid data or passwords do not match."),
        500: openapi.Response("Internal server error."),
    },
)
@api_view(['POST'])
def user_registration_data(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            
            username = body.get('username')
            password = body.get('password')
            c_password = body.get('c_password')
            email = body.get('email')
            mobile = body.get('mobile')
            date_time = timezone.now()
            
            if password != c_password:
                return JsonResponse({'message': 'Passwords do not match.'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email is already registered.'}, status=400)
            
            hashed_password = make_password(password)
            user = User(username=username, password=hashed_password, email=email, mobile=mobile, date_time=date_time)
            user.save()
            
            return JsonResponse({'message': 'Registration successful!'}, status=201)
        
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)