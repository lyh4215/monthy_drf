from .serializers import (
    PostSerializer,
    PostImageSerializer,
    PostCreateSerializer,
    PostImageCreateSerializer
)
from .models import Post, PostImage
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        address = self.kwargs.get('address')

        author = User.objects.get(address=address)
        if (author is None):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        queryset = super().get_queryset().filter(author__address=address)

        # filter by published 
        user = self.request.user
        if (user.is_anonymous or user.address != author.address):
            queryset = queryset.filter(published=True)
        
        # filter by year and month
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None and month is not None:
            try:
                year = int(year)
                month = int(month)
                assert 1 <= month <= 12
                queryset = queryset.filter(date__month=month, date__year=year)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return queryset.order_by('date')


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostImageCreateAPIView(generics.CreateAPIView):
    serializer_class = PostImageCreateSerializer

class PostImageRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()
    

    def get_object(self):
        address = self.request.query_params.get('address')
        date = self.request.query_params.get('date')
        device_id = self.request.query_params.get('device_id')
        index = self.request.query_params.get('index')
        if not all([address, date, device_id, index]):
            raise ValidationError({
                'error': '필수 매개변수가 누락되었습니다.',
                'required_params': ['address', 'date', 'device_id', 'index']
            })
        
        try:
            user = User.objects.get(address=address)
        except User.DoesNotExist:
            raise ValidationError({'error': 'not proper address'})
        partial_src = f'images/{user.username}/{date}/{device_id}/{index}'
        post_image = get_object_or_404(PostImage, src__contains=partial_src)
        return post_image

