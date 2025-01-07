from rest_framework import serializers

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    c_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    mobile = serializers.CharField(required=True)
