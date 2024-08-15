from .serializers import (
    PostSerializer,
    PostImageSerializer,
    PostCreateSerializer,
    PostImageCreateSerializer,
    PostUpdatedAtSerializer,

)
from .models import Post, PostImage, PostUpdatedAt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from rest_framework.permissions import AllowAny
from .permissions import IsAuthor

from django.shortcuts import get_object_or_404
from nudge.llm.persona_utils import modify_persona, get_nudge_necessity
from nudge.llm.nudge_utils import make_nudge
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
                local_image_link = get_local_image_link(post_image, author)
                image_link = get_image_link(post_image, author)
                modified_post.pages = modified_post.pages.replace(local_image_link, image_link)
            modified_posts.append(modified_post)
        
        # Serialize the modified posts
        sorted_posts = sorted(modified_posts, key=lambda x: x.date)
        serializer = self.get_serializer(sorted_posts, many=True)
        return Response(serializer.data)


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        post: Post= serializer.instance
        #post에 존재하지 않고, db상에만 존재하는 image 삭제
        updateDeletedImage(post, request.user)
        self.nudge_necessity = get_nudge_necessity(post)

        response_data = serializer.data
        response_data['nudge_necessity'] = self.nudge_necessity
        
        #TODO : Celery 설정
        modify_persona(post)
        if self.nudge_necessity:
            make_nudge(post.author)

        headers = self.get_success_headers(serializer.data)
        response = Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        return response

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthor]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        post: Post = self.get_object()
        #post에 존재하지 않고, db상에만 존재하는 image 삭제
        updateDeletedImage(post, request.user)

        self.nudge_necessity = get_nudge_necessity(post)
        response.data['nudge_necessity'] = self.nudge_necessity
        modify_persona(post)
        if self.nudge_necessity:
            make_nudge(post.author)
        return response

class PostImageCreateAPIView(generics.CreateAPIView):
    serializer_class = PostImageCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'date': self.kwargs['date'],
            'name_hash': self.kwargs['name_hash'],
            'device_id': self.kwargs['device_id'],
        })
        return context

class PostUpdatedAtAPIView(generics.RetrieveAPIView):
    queryset = PostUpdatedAt.objects.all()
    serializer_class = PostUpdatedAtSerializer
    permission_classes = [IsAuthor]

    def get_object(self):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        user = self.request.user
        queryset = self.get_queryset().filter(author=user, month = month, year = year)
        obj, created = PostUpdatedAt.objects.get_or_create(
            author=user,
            month = month,
            year = year,
        )
        return obj

def updateDeletedImage(post: Post, author: User):
    post_images = post.images.all()
    for post_image in post_images:
        local_image_link = get_local_image_link(post_image, author)
        if local_image_link not in post.pages:
            post_image.delete()

def get_local_image_link(post_image: PostImage, author : User):
    src = post_image.src.name
    return src.replace(f'images/{author.username}/', 'images/')

def get_image_link(post_image: PostImage, author : User):
    src = post_image.src.name
    base_url = settings.AWS_S3_CUSTOM_DOMAIN
    return f'https://{base_url}/{src}'

