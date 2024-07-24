from rest_framework import serializers
from .models import Post, PostImage
from accounts.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']

    def validate_date(self, value):
        author = self.context['request'].user
        if Post.objects.filter(date=value, author=author).exists():
            existingPost = Post.objects.get(date=value, author=author)
            raise serializers.ValidationError(existingPost.pk)
        return value

    def create(self, validated_data):
        address = self.context['request'].data['address']
        validated_data['author'] = User.objects.get(address=address)
        return super().create(validated_data)
    

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

class PostWithImageSerializer(serializers.Serializer):
    post = PostSerializer()
    images = PostImageSerializer(many=True)

    def create(self, validated_data):
        post_data = validated_data.pop('post')
        images_data = validated_data.pop('images')
        post = Post.objects.create(**post_data)
        for image_data in images_data:
            PostImage.objects.create(post=post, **image_data)
        return {
            'post': post,
            'images': images_data
        }
