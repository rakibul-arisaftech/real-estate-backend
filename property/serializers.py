from .models import Property
from rest_framework import serializers

class PropertyReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Property
        # fields = ('id', 'title', 'size', 'location', 'rooms', 'baths', 'price', 'description', 'author')
        fields = "__all__"

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)


class PropertyWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Property
        # fields = ('id', 'title', 'size', 'location', 'rooms', 'baths', 'price', 'description', 'author')
        fields = "__all__"