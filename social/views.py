from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Friend
from .serializers import FriendSerializer, FriendSendSerializer
from .permissions import IsFriendSender, IsFriendReceiver
from django.contrib.auth import get_user_model

User = get_user_model()

class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer

class FriendSendViewSet(FriendViewSet):
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
    
    
class FriendReceiveViewSet(FriendViewSet):
    permission_classes = [IsFriendReceiver]
    lookup_field = 'friend'
    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(friend=user)
    
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("Create")

    
