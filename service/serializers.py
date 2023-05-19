from .models import Service
from rest_framework import serializers

class ServiceReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Service
        fields = "__all__"
        # fields = ('id', 'title', 'description', 'author')


class ServiceWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Service
        fields = "__all__"
        # fields = ('id', 'title', 'description', 'author')