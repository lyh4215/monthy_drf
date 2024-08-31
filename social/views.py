from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from .models import Friend, BlockedUser
from .serializers import FriendSendSerializer, FriendReceiveSerializer, BlockedUserSerializer
from .permissions import IsFriendSender, IsFriendReceiver, IsBlocker
from django.contrib.auth import get_user_model


User = get_user_model()

class FriendSendViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = FriendSendSerializer
    permission_classes = [IsFriendSender]
    lookup_field = 'friend__address'
    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class FriendReceiveViewSet(mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [IsFriendReceiver]
    lookup_field = 'user__address'
    serializer_class = FriendReceiveSerializer
    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(friend=user)
    
    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        if friend_request.status == 'pending':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'status': 'accepted'}, status=status.HTTP_200_OK)
        elif friend_request.status == 'accepted':
            return Response({'status': 'already accepted'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    
class BlockedUserViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = BlockedUserSerializer
    permission_classes = [IsBlocker]
    lookup_field = 'blocked_user__address'
    def get_queryset(self):
        user = self.request.user
        return BlockedUser.objects.filter(blocker=user)
    
    def perform_create(self, serializer):
        serializer.save(blocker=self.request.user)