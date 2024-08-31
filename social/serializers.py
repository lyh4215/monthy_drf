from rest_framework import serializers
from .models import Friend
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['user', 'friend', 'status']
        read_only_fields = ['status']

class FriendSendSerializer(serializers.ModelSerializer):
    friend = serializers.SlugRelatedField(slug_field='address', queryset=User.objects.all())

    def validate(self, data):
        user = self.context['request'].user
        friend = data['friend']
        if Friend.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError("Friend request already sent.")
        return data
    
    class Meta:
        model = Friend
        fields = ['friend', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

class FriendReceiveSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='address', queryset=User.objects.all())

    class Meta:
        model = Friend
        fields = ['user', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']