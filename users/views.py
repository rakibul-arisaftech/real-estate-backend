from . import serializers
from .models import Profile, Wishlist
from rest_framework import status, viewsets, permissions
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView

from .permissions import IsAuthorOrReadOnly

User = get_user_model()

api_view(['GET'])
def health_check(request):
    return JsonResponse({"message": "everything is working fine"})

class UserRegistrationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
        # else:
            for field_name, field_errors in serializer.errors.items():
                return Response({
                    'status_code': 409,
                    'message': field_errors[0]
                    }, status=status.HTTP_409_CONFLICT)



class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            serializer = serializers.CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            return Response({
                'status_code': 401,
                'message': 'invalid credential'
                }, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """

    queryset = Profile.objects.all()
    # serializer_class = serializers.ProfileSerializer
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return serializers.ProfileWriteSerializer
        elif self.request.method == "GET":
            return serializers.ProfileReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

# class ProfileViewSet(viewsets.ModelViewSet):
#     """
#     UPDATE profile
#     """

#     queryset = Profile.objects.all()

#     def get_serializer_class(self):
#         if self.action in ("update", "partial_update"):
#             return serializers.ProfileWriteSerializer

#         return serializers.ProfileWriteSerializer

#     def get_permissions(self):
#         if self.action in ("update", "partial_update"):
#             self.permission_classes = (IsAuthorOrReadOnly,)
#         else:
#             self.permission_classes = (IsAuthorOrReadOnly,)

#         return super().get_permissions()

# class WishlistView(APIView):
#     """
#     Create, Get, Delete wishlist 
#     """

#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         serializer = serializers.WishlistSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def get(self, request, format=None):
#         wishlist = Wishlist.objects.all()
#         serializer = serializers.WishlistSerializer(wishlist, many=True)
#         return Response(serializer.data)
    


class WishlistViewSet(viewsets.ModelViewSet):
    """
    CRUD wishlist
    """

    queryset = Wishlist.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.WishlistWriteSerializer

        return serializers.WishlistReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (IsAuthorOrReadOnly,)

        return super().get_permissions()
