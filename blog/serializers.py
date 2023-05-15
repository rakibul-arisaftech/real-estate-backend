from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username')

class CommentSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('id','content', 'author', 'post')

class PostSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['id', 'title', 'post_date', 'content', 'tags', 'fb', 'twitter']
