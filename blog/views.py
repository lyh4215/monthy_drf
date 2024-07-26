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

from django.conf import settings


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        author = self.request.user
        queryset = super().get_queryset().filter(author=author)

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


def get_origin_image_link(post_image: PostImage, author : User):
    src = post_image.src.name
    return src.replace(f'images/{author.username}/', 'images/')

def get_image_link(post_image: PostImage, author : User):
    src = post_image.src.name
    base_url = settings.AWS_S3_CUSTOM_DOMAIN
    return f'https://{base_url}/{src}'

class PostListWithImageLinkAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        address = self.kwargs.get('address')
        author = get_object_or_404(User, address=address)

        queryset = self.get_queryset().filter(author__address=address)

        # filter by published
        user = self.request.user
        if user.is_anonymous or user.address != author.address:
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

        # Create a list to hold the modified posts
        modified_posts = []
        for post in queryset:
            modified_post = post
            for post_image in post.images.all():
                origin_image_link = get_origin_image_link(post_image, author)
                image_link = get_image_link(post_image, author)
                modified_post.body = modified_post.body.replace(origin_image_link, image_link)
            modified_posts.append(modified_post)
        
        sorted_posts = sorted(modified_posts, key=lambda x: x.date)

        # Serialize the modified posts
        serializer = self.get_serializer(sorted_posts, many=True)
        return Response(serializer.data)


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostImageCreateAPIView(generics.CreateAPIView):
    serializer_class = PostImageCreateSerializer

class PostImageDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()
    
    def get_object(self):
        author = self.request.user
        date = self.request.query_params.get('date')
        device_id = self.request.query_params.get('device_id')
        index = self.request.query_params.get('index')
        if not all([date, device_id, index]):
            raise ValidationError({
                'error': 'wrong params',
                'required_params': ['date', 'device_id', 'index']
            })
        partial_src = f'images/{author.username}/{date}/{device_id}/{index}'
        post_image = get_object_or_404(PostImage, src__contains=partial_src)
        return post_image

class PostImageRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()

    def get_object(self):
        address = self.request.query_params.get('address')
        date = self.request.query_params.get('date')
        device_id = self.request.query_params.get('device_id')
        index = self.request.query_params.get('index')
        if not all([address, date, device_id, index]):
            raise ValidationError({
                'error': 'wrong params',
                'required_params': ['address', 'date', 'device_id', 'index']
            })
        try:
            user = User.objects.get(address=address)
        except User.DoesNotExist:
            raise ValidationError({'error': 'not proper address'})
        partial_src = f'images/{user.username}/{date}/{device_id}/{index}'
        post_image = get_object_or_404(PostImage, src__contains=partial_src)
        return post_image

