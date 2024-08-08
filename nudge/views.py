from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.utils import timezone
from nudge.models import Nudge
from nudge.serializers import NudgeSerializer
from nudge.permissions import IsAuthor
# Create your views here.
class NudgeRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Nudge.objects.all()
    serializer_class = NudgeSerializer

    def get_queryset(self):
        author = self.request.user
        return Nudge.objects.filter(author=author).order_by('-created_at')
    
    def get_object(self):
        queryset = self.get_queryset()
        nudge = queryset.first()
        if nudge.date < timezone.now():
            raise NotFound(detail="All pending nudges are expired")
        elif nudge.status != Nudge.Status.PENDING:
            raise NotFound(detail="There is no pending nudge")
        else:
            #TODO: renew date with agent
            return nudge
        
class ConfirmNudgeAPIView(APIView):
    permission_classes = [IsAuthor]

    def get(self, request, *args, **kwargs):
        nudge = get_object_or_404(Nudge, pk=self.kwargs['pk'])
        nudge.status = Nudge.Status.CONFIRMED
        nudge.save()
        return Response({'message': 'Nudge confirmed'})
    
class RejectNudgeAPIView(APIView):
    permission_classes = [IsAuthor]

    def get(self, request, *args, **kwargs):
        nudge = get_object_or_404(Nudge, pk=self.kwargs['pk'])
        nudge.status = Nudge.Status.REJECTED
        nudge.save()
        return Response({'message': 'Nudge rejected'})