from rest_framework import serializers
from .models import Post, PostImage, PostUpdatedAt
from accounts.models import User
import uuid
import base64


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'author']


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


class PostImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['src', 'post', 'name_hash', 'device_id']
        read_only_fields = ['post', 'name_hash', 'device_id']

    def validate_date(self, value):
        author = self.context['request'].user
        if not Post.objects.filter(date=value, author=author).exists():
            #TODO : add template (prepare about not expected disconnect)
            Post.objects.create(date=value, author=author)
        return value

    def validate_device_id(self, value):
        if not isinstance(value, uuid.UUID):
            raise serializers.ValidationError("Invalid UUID")
        return value

    def create(self, validated_data):
        date = self.context['date']
        name_hash = self.context['name_hash']
        device_id = self.context['device_id']
        author = self.context['request'].user
        post = Post.objects.filter(date=date, author=author).first()
        if not post:
            raise serializers.ValidationError("Post does not exist")
        validated_data['post'] = post
        validated_data['name_hash'] = name_hash
        validated_data['device_id'] = device_id
        return super().create(validated_data)
    
class PostUpdatedAtSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostUpdatedAt
        fields = '__all__'
        read_only_fields = ['author', 'updated_at']