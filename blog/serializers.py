from rest_framework import serializers
from .models import Post, PostImage
from accounts.models import User
import uuid
import base64


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


class PostImageCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(write_only=True)
    class Meta:
        model = PostImage
        fields = ['src', 'device_id', 'name_hash', 'date', 'post']
        read_only_fields = ['post']

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
        date = validated_data.pop('date')
        author = self.context['request'].user
        post = Post.objects.filter(date=date, author=author).first()
        if not post:
            raise serializers.ValidationError("Post does not exist")
        validated_data['post'] = post
        return super().create(validated_data)