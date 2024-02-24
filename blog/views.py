from .serializers import PostSerializer, PostImageSerializer, PostCreateSerializer
from .models import Post
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        address = self.kwargs.get('address')
        if (User.objects.get(address=address) is None):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        queryset = super().get_queryset().filter(author__address=address)
        
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

        ### to add: filter depending on published status
            
        return queryset.order_by('date')


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostImageCreateAPIView(generics.CreateAPIView):
    serializer_class = PostImageSerializer
