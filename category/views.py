from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer
from .models import Category

# Create your views here.
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'POST':
        category = request.data
        serializer = CategorySerializer(data=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    elif request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response({'category': serializer.data})
    

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return Response(
            {'message': 'this category does not exist'}, 
            status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response({"category": serializer.data})
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Successfully Deleted'}, 
                        status=status.HTTP_204_NO_CONTENT)
