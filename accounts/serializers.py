from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'address', 'profile_image', 'enable_publish')

class TokenValidationSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)