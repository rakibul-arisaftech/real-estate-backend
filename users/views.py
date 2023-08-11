from .utils import sending_mail
from . import serializers
from rest_framework import generics
from django.http import JsonResponse
from .models import Profile, Wishlist
from rest_framework.views import APIView
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView

from django.contrib.auth.hashers import make_password

from django.core.mail import send_mail
from django.conf import settings
import random


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
        # try:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
                # user = serializer.save()
                # token = RefreshToken.for_user(user)
            # try:
            serializer.save()
            # except Exception as e:
            #     print(f"this is the prob {e}")
            #     return Response({
            #         'status': 500,
            #         'message': 'internal server error',
            #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            data = serializer.data
            sending_mail(data['email'])
            # data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response({
                    'status': 201,
                    'message': 'registration completed, please check email',
                    'data':data
                    }, status=status.HTTP_201_CREATED)
        else:
            for field_name, field_errors in serializer.errors.items():
                return Response({
                    'status_code': 409,
                    'message': field_errors[0]
                    }, status=status.HTTP_409_CONFLICT)
        # except Exception as e:
        #     for field_name, field_errors in serializer.errors.items():
        #         return Response({
        #             'status_code': 409,
        #             'message': field_errors[0]
        #             }, status=status.HTTP_409_CONFLICT)

class VerifyEmailOTP(APIView):
    def post(self, request):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            email = data['email']
            otp = data['otp']

            user = User.objects.filter(email=email)

            if not user.exists():
                return Response({
                    'status_code': 400,
                    'message': 'invalid email'
                    }, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp != otp:
                return Response({
                    'status_code': 400,
                    'message': 'wrong otp'
                    }, status=status.HTTP_400_BAD_REQUEST)

            if user[0].is_verified == True:
                return Response({
                    'status_code': 200,
                    'message': 'email already verified'
                    }, status=status.HTTP_200_OK)

            user = user.first()
            user.is_verified = True
            user.save()

            return Response({
                    'status': 200,
                    'message': 'account verified'
                    }, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordOTP(GenericAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = serializers.ResetPasswordOTPSerializer
    
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            # data = serializer.data
            subject = 'Your account password reset email'
            otp = random.randint(1000, 9999)
            message = f'Your otp is {otp}'
            email_from = settings.EMAIL_HOST
            send_mail(subject, message, email_from, [request.data['email']])
            user_obj = User.objects.get(email=request.data['email'])
            user_obj.otp = otp
            user_obj.save()
            return Response({
                        'status': 200,
                        'message': 'Reset password OTP sent, please check email'
                        }, status=status.HTTP_200_OK)

class ResetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for resetting password.
    """
    serializer_class = serializers.ResetPasswordSerializer
    model = User
    permission_classes = (AllowAny,)

    def update(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data['email'])[0]
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            # data = serializer.data
            data = {
                "message": "login successfull",
                "user_info": serializer.data,
                "tokens": {"refresh": str(token), "access": str(token.access_token)}
            } 
            # data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            return Response({
                'status_code': 401,
                'message': 'invalid credential'
                }, status=status.HTTP_401_UNAUTHORIZED)


# class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    # permission_classes = (IsAuthenticated,)

    # def post(self, request, *args, **kwargs):
    #     try:
    #         refresh_token = request.data["refresh"]
    #         token = RefreshToken(refresh_token)
    #         token.blacklist()
    #         return Response(status=status.HTTP_205_RESET_CONTENT)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

class LogOutAPIView(APIView):
    def post(self,request,format=None):
        try:
            refresh_token = request.data.get("refresh_token")
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status = status.HTTP_200_OK)
        except Exception as e:
            return Response(status = status.HEEP_400BAD_REQUEST)



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