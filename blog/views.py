from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Category, Comment, Post
from .serializers import (
    CategoryReadSerializer,
    CategoryWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer,
)

from .permissions import IsAuthorOrReadOnly


@api_view(['GET'])
def latest_posts(request):
    if request.method == 'GET':
        posts = Post.objects.order_by('-created_at')[:3]
        serializer = PostReadSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogViewPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 10


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD post categories
    """

    queryset = Category.objects.all()
    # serializer_class = CategoryReadSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CategoryWriteSerializer

        return CategoryReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD posts
    """

    queryset = Post.objects.all()
    pagination_class = BlogViewPagination

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

