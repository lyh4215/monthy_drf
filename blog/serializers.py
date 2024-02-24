from rest_framework import serializers
from .models import Post, PostImage
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        authorname = self.context['request'].data['authorname']
        validated_data['author'] = User.objects.get(username=authorname)
        return super().create(validated_data)
    

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

