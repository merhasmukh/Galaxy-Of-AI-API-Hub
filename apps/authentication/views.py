from django.utils import timezone
from . import custom_auth
from .models import User
from django.contrib.auth.hashers import make_password
import os
import json
import smtplib, ssl
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# from src import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
import logging
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)
FRONTEND_URL=os.getenv("FRONTEND_URL")

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        

        try:
    
            user = custom_auth.CustomAuthBackend.authenticate(request, email=email, password=password)
        
            if 'error' in user:
                logger.error(user['error'])
                return Response({'message': user['error']}, status=status.HTTP_400_BAD_REQUEST)
            
            elif 'success' in user:
                user_id=user['user_object'].id
                username=user['user_object'].username
                phone=user['user_object'].mobile
                dob=user['user_object'].dob
                
                refresh_token = user['refresh_token']
                access_token = user['access_token']
                response_info={'message': 'Login Success',
                               "access_token": access_token,
                               "refresh_token":str(refresh_token),
                               "user_id":user_id,
                               "username":username,
                               "email":email,
                               "phone":phone,
                               "dob":dob,
                                "profile_image": "",

                               }

                return Response(response_info, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'First, You have to register with us..'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(str(e))
            return Response({'message': 'Login Failed! Please Try Again..!!'}, status=status.HTTP_400_BAD_REQUEST)



class GoogleAuthAPIView(APIView):
    """
    Handle Google Sign-In, check if user exists, and update details if needed.
    """
    permission_classes = [AllowAny]  # Allow unauthenticated users to access


    def post(self, request):
        token = request.data.get("token")

        try:
            # Verify the Google token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))

            # Extract user information
            email = idinfo.get("email")
            google_id = idinfo.get("sub")
            username = idinfo.get("name","")

            profile_image = idinfo.get("picture", "")

            if not email:
                return Response({"message": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user already exists
            user, created = User.objects.get_or_create(email=email, defaults={
                "username": username,
                "google_id": google_id,
                "profile_image": profile_image,
                "last_login": timezone.now(),
            })

            # ✅ If user already exists but is missing Google ID, update their info
            if not created:
                if not user.google_id:
                    user.google_id = google_id
                user.profile_image = profile_image  # Always update profile picture
                user.save()

            # Issue JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                "message": "Google Login Success",
                "access_token": access_token,
                "refresh_token": str(refresh),
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": getattr(user, "mobile", None),  
                "dob": getattr(user, "dob", None), 
                "profile_image": user.profile_image,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.error(str(e))
            return Response({"message": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

class TokenValidation(APIView):
    def get(self,request):
        try:
            user = request.user
            return Response({
                "valid": True,
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "valid": False,
                "error": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
def get_user_details(request, user_id):
    try:
        # Access the user from JWT token
        user = request.user  # `request.user` is automatically set by Django Rest Framework after JWT authentication
        
        if user.id == user_id:  # Ensure the user accessing this endpoint is the same user
            user_data = {
                "username": user.username,
                "email": user.email,
                "mobile": user.mobile,
                "file_status": user.file_status,
                "video_status": user.video_status,
                "file_path": user.file_path,
                "video_path": user.video_path,
                "date_time": user.date_time,
                "last_login": user.last_login,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@swagger_auto_schema(methods=['post'], operation_description="This endpoint allows users to register.")
@api_view(['POST'])
@permission_classes([AllowAny])
def user_register_data(request):
    if request.method == 'POST':
        try:
            body = request.data
            username = body.get('name')
            password = body.get('password')
            confirm_password = body.get('confirmPassword')
            email = body.get('email')
            mobile = body.get('phone')
            dob = body.get('dob')


            # Validate required fields
            if not all([username, password, confirm_password, email, mobile]):
                return Response({'message': 'All fields are required.'}, status=400)

            # Check password match
            if password != confirm_password:
                return Response({'message': 'Passwords do not match.'}, status=400)

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return Response({'message': 'Email is already registered.'}, status=400)

            # Hash the password
            hashed_password = make_password(password)

            # Create new user
            user = User(username=username, password=hashed_password, email=email, mobile=mobile, date_time=timezone.now(),dob=dob)
            user.save()

          
            # Return success message and tokens
            return Response({
                'message': 'Registration successful!',
               
            }, status=201)
        
        except Exception as e:
            logger.exception(f"Error during registration: {str(e)}")
            return Response({'message': str(e)}, status=500)
    else:
        return Response({'message': 'Invalid request method.'}, status=405)

@swagger_auto_schema(methods=['post'], operation_description="This endpoint allows users to reset password.")
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = request.data.get('email')
    
    try:
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        reset_link = f"{FRONTEND_URL}/user/reset-password/{user.id}/{token}"
        
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = os.getenv("FROM_EMAIL")
        receiver_email = email 
        password = os.getenv("EMAIL_PASSWORD")
        
        # Subject and body of the email
        subject = "Password Reset Request"
        body = f"Click the link to reset your password: {reset_link}"
        
        # Create a MIMEText object
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        
        # Attach the body to the email
        message.attach(MIMEText(body, "plain"))
        
        # Send the email using SMTP_SSL
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            return JsonResponse({"message": "Password reset link sent to your email."}, status=200)
        except Exception as e:
            logger.exception(str(e))

            return JsonResponse({"error": "Error sending mail: " + str(e)},status=400)
        
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        logger.exception(str(e))
        return JsonResponse({"error": "User not found."}, status=404)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_token(request):
    token = request.data.get('token')
    uid = request.data.get('uid')

    try:
        user = User.objects.get(id=uid)

        uid = default_token_generator.check_token(user,token)
        if uid:
            return JsonResponse({"message": "Token is valid."}, status=200)
        else:
            logger.error(str(uid))
            return JsonResponse({"error": "Invalid or expired token."}, status=400)
    except Exception as e:
        logger.exception(str(e))
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_confirm(request):
    token = request.data.get('token')
    new_password = request.data.get('newPassword')
    uid = request.data.get('uid')

    try:
        user = User.objects.get(id=uid)

        uid = default_token_generator.check_token(user,token)
        if not uid:
            return JsonResponse({"error": "Invalid or expired token."}, status=400)

        user.password = make_password(new_password)
        user.save()

        return JsonResponse({"message": "Password successfully reset."}, status=200)
    except User.DoesNotExist:
        logger.exception(str(e))
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        logger.exception(str(e))
        return JsonResponse({"error": str(e)}, status=400)

    


@swagger_auto_schema(methods=['post'], operation_description="This endpoint allows users to login.")
@api_view(['POST'])
def user_login_data(request):
    
    if request.method == 'POST':
        try:
            body=request.data
            email = body.get('email')
            password = body.get('password')  # Hash the password

            user = custom_auth.CustomAuthBackend.authenticate(request, email=email, password=password)
        
            if 'error' in user:
                return JsonResponse({'message': user['error']}, status=400)
            
        
            elif 'success' in user:
                refresh_token = RefreshToken.for_user(user['user_object'])
                access_token = str(refresh_token.access_token)

                return JsonResponse({'message': 'Login Success',"access_token": access_token,"refresh_token":str(refresh_token)}, status=200)

            else:
                return JsonResponse({'message': 'First, You have to register with us..'}, status=400)
        except Exception as e:
            logger.exception(str(e))
            return JsonResponse({'message': 'Login Failed! Please Try Again..!!'}, status=400)

    else:
        return JsonResponse({'message': 'Login Failed! Please Try Again..!!'}, status=400)
    
 