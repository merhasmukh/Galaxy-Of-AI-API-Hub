from rest_framework import serializers
from .models import Chat,ChatMessages,ResourceManager

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
