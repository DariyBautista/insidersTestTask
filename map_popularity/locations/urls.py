from django.urls import path
from .views import CreateLocationView, LocationDetailView, ExportLocationsView

urlpatterns = [
    path('locations/', CreateLocationView.as_view(), name='create-location'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('locations/export/', ExportLocationsView.as_view(), name='export-locations'),
]
