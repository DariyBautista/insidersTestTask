from django.urls import path
from .views import CreateReviewView

urlpatterns = [
    path('locations/<int:location_id>/reviews/', CreateReviewView.as_view(), name='create-review'),
]
