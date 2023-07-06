from rest_framework import serializers
from .models import CustomUser, Profile, Wishlist
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "is_verified")

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class ProfileReadSerializer(CustomUserSerializer):
    wishlist = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

    def get_wishlist(self, obj):
        wish_lists = Wishlist.objects.filter(user_id=obj.user_id)
        return [i.property_id for i in wish_lists]


class ProfileWriteSerializer(CustomUserSerializer):

    class Meta:
        model = Profile
        fields = "__all__"

class WishlistReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"

class WishlistWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('otp',)

    """
    Serializer for password change endpoint.
    """
    # email = serializers.EmailField(required=True)