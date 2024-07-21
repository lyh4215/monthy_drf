from rest_framework import serializers
from .models import Post, PostImage
from accounts.models import User
from nudge.llm.persona_utils import modify_persona


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
        modify_persona(validated_data['author'].id, validated_data)
        return super().create(validated_data)
    

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

