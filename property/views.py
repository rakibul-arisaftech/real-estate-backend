from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PropertySerializer
from rest_framework import status
from .models import Property

# Create your views here.
@api_view(['GET', 'POST'])
def property_list(request):
    if request.method == 'POST':
        property_ = request.data
        serializer = PropertySerializer(data=property_)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    elif request.method == 'GET':
        property_ = Property.objects.all()
        serializer = PropertySerializer(property_, many=True)
        return Response({"property": serializer.data})


@api_view(['GET', 'PUT', 'DELETE'])
def property_detail(request, id):
    try:
        property_ = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        return Response(
            {'message': 'this property does not exist'}, 
            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertySerializer(property_)
        return Response({"property": serializer.data})

    elif request.method == 'PUT':
        serializer = PropertySerializer(property_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        property_.delete()
        return Response({'message': 'Successfully Deleted'}, 
                        status=status.HTTP_204_NO_CONTENT)