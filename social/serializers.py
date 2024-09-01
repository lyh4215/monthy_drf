from rest_framework import serializers
from .models import Friend, BlockedUser
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSearchSerializer(serializers.ModelSerializer):
    friend_status = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['address', 'profile_image', 'friend_status']
        read_only_fields = ['friend_status', 'address', 'profile_image']
    def get_friend_status(self, obj):
        user = self.context['request'].user
        friend_status = {}
        try:
            friend_send = Friend.objects.get(user=user, friend=obj)
            friend_status['send'] = friend_send.status
        except:
            friend_status['send'] = None
        try:
            friend_receive = Friend.objects.get(user=obj, friend=user)
            friend_status['receive'] = friend_receive.status
        except:
            friend_status['receive'] = None
        return friend_status

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