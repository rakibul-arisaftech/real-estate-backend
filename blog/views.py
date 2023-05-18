from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets

from .models import Category, Comment, Post
from .serializers import (
    CategoryReadSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer,
)

from .permissions import IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD post categories
    """

    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD posts
    """

    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostWriteSerializer

        return PostReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD comments for a particular post
    """

    queryset = Comment.objects.all()

    def get_queryset(self):
        res = super().get_queryset()
        post_id = self.kwargs.get("post_id")
        return res.filter(post__id=post_id)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentWriteSerializer

        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

