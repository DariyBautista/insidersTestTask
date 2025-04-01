from rest_framework import serializers
from .models import Review
from locations.models import Location
from django.contrib.auth import get_user_model
from locations.serializers import LocationSerializer

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    
    location = LocationSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    action = serializers.ChoiceField(choices=['like', 'dislike'], write_only=True, required=False)

    class Meta:
        model = Review
        fields = ['id', 'location', 'user', 'text', 'action', 'likes', 'dislikes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Review text cannot be empty.")
        return value

    def validate_likes(self, value):
        if value < 0:
            raise serializers.ValidationError("Likes cannot be negative.")
        return value

    def validate_dislikes(self, value):
        if value < 0:
            raise serializers.ValidationError("Dislikes cannot be negative.")
        return value
