from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os
from dotenv import load_dotenv
from rest_framework.permissions import AllowAny
from .src.helper_function import generate_galaxy_ai_chatbot_prompt

# Load API Key from environment variables
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GENAI_API_KEY)
# Create your views here.
class GeminiAIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        try:
            user_message = request.data.get("message", "").strip()

            if not user_message:
                return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

            client = genai.GenerativeModel("gemini-2.0-flash")
            system_prompt=generate_galaxy_ai_chatbot_prompt(user_message)
            response = client.generate_content(system_prompt)

            return Response({"message": response.text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)