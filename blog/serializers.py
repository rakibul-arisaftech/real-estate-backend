from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source = 'user.username')
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )

    class Meta:
        model = Post
        fields = ('title', 'post_date', 'content', 'tags', 'fb', 'twitter', 'user')


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source = 'user.username')

    class Meta:
        model = Comment
        fields = ('post', 'author', 'content', 'created_at', 'user')
