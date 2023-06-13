from rest_framework import serializers
from .models import CustomUser, Profile, Wishlist
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    class Meta:
        model = CustomUser
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
    

# class ProfileSerializer(CustomUserSerializer):
#     """
#     Serializer class to serialize the user Profile model
#     """
    
#     class Meta:
#         model = Profile
#         fields = '__all__'

# class WishlistSerializer(serializers.ModelSerializer):
#     """
#     Serializer class to serialize the user Wishlist model
#     """

#     class Meta:
#         model = Wishlist
#         fields = '__all__'


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