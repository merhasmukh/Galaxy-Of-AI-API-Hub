from rest_framework import serializers
from .models import Chat,ChatMessages,ResourceManager,WorkLog

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'chat_id', 'timestamp','name','description','language']



class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = ["id", "question", "answer", "timestamp"]


class ChatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'description', 'language']



class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceManager
        fields = ['id', 'title', 'url', 'type']




class WorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLog
        fields = ['id', 'date', 'start_time', 'end_time', 'duration_hours', 'description']
