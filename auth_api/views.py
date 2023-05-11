from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
import os

# HEALTH CHECK
class HealthCheckAPI(generics.GenericAPIView):
    def get(self, request):
        print(os.environ.get('DB_NAME'))
        return Response({'status': 'everything is working fine'})

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if user:
            login(request, user)
            return super(LoginAPI, self).post(request, format=None)

        return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)        

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)