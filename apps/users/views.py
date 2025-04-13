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
from .prompts.ai_research_prompt import generate_ai_research_helper_prompt,generate_independent_ai_research_prompt
from .models import Chat,ChatMessages
import uuid
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

            client = genai.GenerativeModel("gemini-2.0-flash")
            system_prompt=generate_independent_ai_research_prompt(user_message)

            response = client.generate_content(system_prompt)
            answer=response.text
            ChatMessages.objects.create(chat_id=chat_id, question=user_message, answer=answer)

            return Response({"message": answer}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)