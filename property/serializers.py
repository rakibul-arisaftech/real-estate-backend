from .models import Property
from rest_framework import serializers

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'title', 'size', 'location', 'rooms', 'baths', 'price', 'description')
        # fields = '__all__'
