from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os
from dotenv import load_dotenv
from rest_framework.permissions import AllowAny
from .prompts.main_prompt import generate_main_prompt
from .prompts.ai_research_prompt import generate_ai_research_helper_prompt
from .models import Chat,ChatMessages,ResourceManager
import uuid
import re
from .serializer import ChatSerializer,ChatMessageSerializer,ChatUpdateSerializer,ResourceSerializer
# Load API Key from environment variables
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GENAI_API_KEY)
# Create your views here.
class GeminiAIView(APIView):

    def post(self, request):
        try:
            user_id = request.user.id
            chat_id = request.data.get("chat_id")
            user_message = request.data.get("message", "").strip()

            if not user_message:
                return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not chat_id:
                chat_id = str(uuid.uuid4())  # generate unique chat id
                Chat.objects.create(user_id=user_id, chat_id=chat_id)

            
            history = []
            if chat_id:
                past_msgs = ChatMessages.objects.filter(chat_id=chat_id).order_by("-timestamp")[:10][::-1]
            
                for msg in past_msgs:
                    history.append({"role": "user", "parts": [{"text": msg.question}]})
                    history.append({"role": "model", "parts": [{"text": msg.answer}]})
                
            try:
                chat = Chat.objects.get(chat_id=chat_id)
            except Chat.DoesNotExist:
                return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

            # Add current message from user
            history.append({"role": "user", "parts": [{"text": user_message}]})
            print("History:",history)
            client = genai.GenerativeModel("gemini-2.0-flash")
            system_prompt=generate_ai_research_helper_prompt(user_message,history,language=chat.language,assistant_name=chat.name,project_description=chat.description)

            response = client.generate_content(system_prompt)
            answer=response.text.strip()

            ChatMessages.objects.create(chat_id=chat_id, question=user_message, answer=answer)

            return Response({"message": answer,"chat_id":chat_id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChatList(APIView):

    def get(self, request):
        try:
            user_id = request.user.id
            
            chats = Chat.objects.filter(user_id=user_id).order_by('-timestamp')
            serialized = ChatSerializer(chats, many=True)


            return Response({"chats": serialized.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChatHistory(APIView):

    def get(self, request,chat_id):
        try:
            user_id = request.user.id

            if not chat_id:
                return Response({"error": "Chat Id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
            if not Chat.objects.filter(chat_id=chat_id, user_id=user_id).exists():
                return Response({"error": "Chat not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

            messages = ChatMessages.objects.filter(chat_id=chat_id).order_by("timestamp")
            serialized = ChatMessageSerializer(messages, many=True)
            



        
            return Response({"chats": serialized.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChatUpdateAPIView(APIView):
    def post(self, request, chat_id):
        try:
            chat = Chat.objects.get(chat_id=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatUpdateSerializer(chat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Chat updated successfully", "chat": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResourceAPIView(APIView):
    def get(self, request):
        resources = ResourceManager.objects.all().order_by('-id')
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Resource added successfully", "resource": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
