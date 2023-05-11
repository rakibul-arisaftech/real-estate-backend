from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ServiceSerializer
from .models import Service
from django.http import JsonResponse
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def create_service(request):
    if request.method == 'POST':
        service = request.data
        serializer = ServiceSerializer(data=service)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "An error has occurred"}, status=status.HTTP_502_BAD_GATEWAY)

@api_view(['GET'])
def get_services(request):
    if request.method == 'GET':
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response({"services": serializer.data})
    
@api_view(['GET'])
def get_service(request, id, format=None):
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ServiceSerializer(data=service)
        return Response({"post": serializer.data})
    
@api_view(['PUT'])
def update_service(request, id, format=None):
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['DELETE'])
def delete_service(request, id, format=None):
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)