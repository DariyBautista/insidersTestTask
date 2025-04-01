from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from django.db.models import Q
from django.http import HttpResponse
import pandas as pd
from rest_framework.views import APIView
from .models import Location
from .serializers import LocationSerializer
from django.http import JsonResponse, HttpResponse
from django.views import View
import json

class CreateLocationView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Location.objects.all()
        rating_min = self.request.query_params.get('rating_min')
        rating_max = self.request.query_params.get('rating_max')
        category = self.request.query_params.get('category')
        search_query = self.request.query_params.get('search')

        if rating_min is not None:
            queryset = queryset.filter(rating__gte=rating_min)
        if rating_max is not None:
            queryset = queryset.filter(rating__lte=rating_max)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        return queryset.order_by('-created_at')


class LocationDetailView(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ExportLocationsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        format_type = request.GET.get('format', 'json')
        download = request.GET.get('download', 'false').lower() == 'true'
        locations = Location.objects.all()

        if format_type == 'csv':
            df = pd.DataFrame(list(locations.values()))

            if download:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="locations.csv"'
                df.to_csv(path_or_buf=response, index=False)
                return response
            else:
                return JsonResponse(df.to_dict(orient='records'), safe=False)

        elif format_type == 'json':
            serializer = LocationSerializer(locations, many=True)
            data = json.dumps(serializer.data, indent=4)

            if download:
                response = HttpResponse(data, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="locations.json"'
                return response
            else:
                return JsonResponse(serializer.data, safe=False)

        return JsonResponse(
            {"detail": "Invalid format specified. Use 'json' or 'csv'."}, 
            status=400
        )

