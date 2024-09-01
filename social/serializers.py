from rest_framework import serializers
from .models import Friend, BlockedUser
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['address', 'profile_image']

class FriendSendSerializer(serializers.ModelSerializer):
    friend = serializers.SlugRelatedField(slug_field='address', queryset=User.objects.all())

    def validate(self, data):
        user = self.context['request'].user
        friend = data['friend']
        if user == friend:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")
        if Friend.objects.filter(user=user, friend=friend).exists():
            if Friend.objects.get(user=user, friend=friend).status == Friend.Status.PENDING:
                raise serializers.ValidationError("Friend request already sent.")
            elif Friend.objects.get(user=user, friend=friend).status == Friend.Status.ACCEPTED:
                raise serializers.ValidationError("Friend request already accepted.")
            else:
                raise serializers.ValidationError("Serializer error")
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

class BlockedUserSerializer(serializers.ModelSerializer):
    blocked_user = serializers.SlugRelatedField(slug_field='address', queryset=User.objects.all())

    def validate(self, data):
        user = self.context['request'].user
        blocked_user = data['blocked_user']
        if user == blocked_user:
            raise serializers.ValidationError("You cannot block yourself.")
        if BlockedUser.objects.filter(blocker=user, blocked_user=blocked_user).exists():
            raise serializers.ValidationError("User already blocked.")
        return data

    class Meta:
        model = BlockedUser
        fields = ['blocked_user', 'created_at']
        read_only_fields = ['created_at']