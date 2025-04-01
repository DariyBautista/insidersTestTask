from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'category', 'rating', 'created_at', 'updated_at', 'user', 'country', 'city', 'latitude', 'longitude']
        read_only_fields = ['id', 'rating', 'created_at', 'updated_at', 'user']

    def validate_name(self, value):
        if self.instance is None and Location.objects.filter(name=value).exists():
            raise serializers.ValidationError("This location already exists.")
        return value

