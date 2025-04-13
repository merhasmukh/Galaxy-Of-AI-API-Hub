from django.urls import path
from .views import GeminiAIView

urlpatterns = [
    path('galaxy_ai_agent/', GeminiAIView.as_view(), name='geminiai_chat'),
    path('user_ai_agent/', GeminiAIView.as_view(), name='user_ai_chat'),

]
