from .serializers import PostSerializer, PostImageSerializer, PostCreateSerializer
from .models import Post
from rest_framework import generics


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        queryset = super().get_queryset().filter(author__username=username)
        
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None and month is not None:
            try:
                year = int(year)
                month = int(month)
                queryset = queryset.filter(date__month=month, date__year=year)
            except ValueError:
                ### to add: raise error
                pass

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
