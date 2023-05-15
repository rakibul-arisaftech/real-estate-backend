from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework import status
from .models import Post

# Create your views here.
@api_view(['POST', 'GET'])
def post_list(request):
    if request.method == 'POST':
        # if request.user.is_active:
        serializer = PostSerializer(data=request.data)
        print(f'create post {serializer.is_valid()}')
        if serializer.is_valid():
            # serializer.save(user=request.user.username)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({"posts": serializer.data})
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(
            {'message': 'this post does not exist'}, 
            status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response({"post": serializer.data})
    
    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE':
        post.delete()
        return Response({'message': 'Successfully Deleted'}, 
                        status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)