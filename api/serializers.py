from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Register, Login, Service, Blog, Category, Property


# Service Serializer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

# Blog Serializer
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Property Serializer
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'

# Login Serializer
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'