from .models import Category
from rest_framework import serializers


class CategoryReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Category
        # fields = "__all__"
        fields = ('id', 'title', 'num_of_elements', 'author')


class CategoryWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        # fields = "__all__"
        fields = ('id', 'title', 'num_of_elements', 'author')