from django.urls import path
from .views import GeminiAIView

urlpatterns = [
    path('user_ai_agent/', GeminiAIView.as_view(), name='user_ai_chat'),

]
