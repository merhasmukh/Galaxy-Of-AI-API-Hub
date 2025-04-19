from django.urls import path
from .views import GeminiAIView,ChatList,ChatHistory,ChatUpdateAPIView,ResourceAPIView,WorkLogAPIView,MilestoneAPIView, MilestoneUpdateDeleteAPIView

urlpatterns = [
    path('chat/ai_agent/', GeminiAIView.as_view(), name='user_ai_chat'),
    path('chat/list/', ChatList.as_view(), name='chat_list'),
    path('chat/history/<str:chat_id>/', ChatHistory.as_view(), name='chat_history'),
    path('chat/update/<str:chat_id>/', ChatUpdateAPIView.as_view(), name='chat-update'),
    path('resources/', ResourceAPIView.as_view(), name='resources'),
    path('worklogs/', WorkLogAPIView.as_view(), name='worklog-api'),
     path('milestones/', MilestoneAPIView.as_view(), name='milestones'),
    path('milestones/<int:pk>/', MilestoneUpdateDeleteAPIView.as_view(), name='milestone-detail'),






]
