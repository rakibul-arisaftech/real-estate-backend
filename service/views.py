from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ServiceSerializer
from rest_framework import status
from .models import Service

# Create your views here.
@api_view(['GET', 'POST'])
def service_list(request):
    if request.method == 'POST':
        service = request.data
        serializer = ServiceSerializer(data=service)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    if request.method == 'GET':
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response({"services": serializer.data})
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, id):
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response({'message': 'this post does not exist'}, 
                        status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response({"service": serializer.data})
    
    if request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE':
        service.delete()
        return Response({'message': 'Successfully Deleted'}, 
                        status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)