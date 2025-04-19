from rest_framework import serializers
from .models import Chat,ChatMessages,ResourceManager,WorkLog,Projects

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        read_only_fields = ['created_at', 'updated_at']
        fields = ['id', 'chat_id', 'name','description','language', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = ["id", "question", "answer", "created_at"]


class ChatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'description', 'language']



class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceManager
        fields = ['id', 'title', 'url', 'type', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']





class WorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLog
        fields = ['id', 'date', 'start_time', 'end_time', 'duration_hours', 'description','created_at']


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'status', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

