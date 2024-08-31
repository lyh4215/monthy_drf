from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Friend
from .serializers import FriendSerializer
from .permissions import IsFriendSender, IsFriendReceiver
# Create your views here.
class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    lookup_field = 'address'


class FriendSendViewSet(FriendViewSet):
    permission_classes = [IsFriendSender]

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(user=user)
    
    
class FriendReceiveViewSet(FriendViewSet):
    permission_classes = [IsFriendReceiver]

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(friend=user)
