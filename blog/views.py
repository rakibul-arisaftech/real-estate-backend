from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        if request.user.is_active:
            # user = request.user
            # print(f"create_post user: {user}")
            # post = request.data
            # print(f"create_post post: {post}")
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                # serializer.save(user=request.user.username)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_posts(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({"posts": serializer.data})
    
@api_view(['GET'])
def get_post(request, id, format=None):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PostSerializer(data=post)
        return Response({"post": serializer.data})
    
@api_view(['PUT'])
def update_post(request, id, format=None):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['DELETE'])
def delete_post(request, id, format=None):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)