from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_details = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_details', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    author_details = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_details', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class LikeSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'user_details', 'post', 'created_at')
        read_only_fields = ('id', 'created_at', 'user')

