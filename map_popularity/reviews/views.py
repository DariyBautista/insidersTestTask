from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from locations.models import Location
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics


class CreateReviewView(LoginRequiredMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer 

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        return Review.objects.filter(location_id=location_id) 

    def get(self, request, location_id):

        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({'detail': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)

        reviews = self.get_queryset() 
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, location_id):
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({'detail': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        text = request.data.get('text')

        if action not in ['like', 'dislike']:
            return Response({'detail': 'Invalid action. Use "like" or "dislike".'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not text or not text.strip():
            return Response({'detail': 'Text of the review is required.'}, status=status.HTTP_400_BAD_REQUEST)

        review, created = Review.objects.get_or_create(location=location, user=request.user)
        if action == 'like':
            review.likes += 1
            review.dislikes = max(0, review.dislikes - 1)
        elif action == 'dislike':
            review.dislikes += 1
            review.likes = max(0, review.likes - 1)
        review.text = text
        review.save()
        review_serializer = ReviewSerializer(review)
        return Response(review_serializer.data, status=status.HTTP_200_OK)
