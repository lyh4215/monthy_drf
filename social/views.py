from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from .models import Friend, BlockedUser
from .serializers import FriendSendSerializer, FriendReceiveSerializer, BlockedUserSerializer, UserSearchSerializer
from .permissions import IsFriendSender, IsFriendReceiver, IsBlocker
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class UserSearchPagination(PageNumberPagination):
    page_size = 10

class UserSearchListAPIView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    pagination_class = UserSearchPagination
    
    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.exclude(address=user.address)

        #exclude not published users
        queryset = queryset.filter(enable_publish=True)
        
        #blocked by user
        blockers = BlockedUser.objects.filter(blocked_user=user).values_list('blocker__address', flat=True)
        queryset = queryset.exclude(address__in=blockers)

        #search
        query = self.request.query_params.get('query', '')
        if query:
            queryset = queryset.filter(address__icontains=query)
        else: #invalid search
            queryset = User.objects.none()

        return queryset

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
        raise MethodNotAllowed("PUT method is not allowed. Use PATCH for partial updates.")
    
    def partial_update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        if friend_request.status == Friend.Status.PENDING:
            friend_request.status = Friend.Status.ACCEPTED
            friend_request.save()
            return Response({'status': 'accepted'}, status=status.HTTP_200_OK)
        elif friend_request.status == Friend.Status.ACCEPTED:
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
        blocked_user = serializer.validated_data['blocked_user']
        blocker = self.request.user
        
        #delete friend
        Friend.objects.filter(user=blocker, friend=blocked_user).delete()
        Friend.objects.filter(user=blocked_user, friend=blocker).delete()
        
        serializer.save(blocker=blocker)