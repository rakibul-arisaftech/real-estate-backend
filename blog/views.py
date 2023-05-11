from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post

# Create your views here.
@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        post = request.data
        serializer = PostSerializer(data=post)
        if serializer.is_valid():
            serializer.save(user=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "An error has occurred"}, status=status.HTTP_502_BAD_GATEWAY)

@api_view(['GET'])
def get_posts(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(data=posts, many=True)
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