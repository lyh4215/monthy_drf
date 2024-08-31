from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from .models import Friend
from .serializers import FriendSerializer, FriendSendSerializer, FriendReceiveSerializer
from .permissions import IsFriendSender, IsFriendReceiver
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendSendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSendSerializer
    permission_classes = [IsFriendSender]
    lookup_field = 'friend__address'
    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("Update")
    
    
class FriendReceiveViewSet(viewsets.ModelViewSet):
    permission_classes = [IsFriendReceiver]
    lookup_field = 'user__address'
    serializer_class = FriendReceiveSerializer
    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(friend=user)
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("Create")
    
    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        if friend_request.status == 'pending':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'status': 'accepted'}, status=status.HTTP_200_OK)
        elif friend_request.status == 'accepted':
            return Response({'status': 'already accepted'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    
