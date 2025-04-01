from django.db import models
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True) 
    def __str__(self):
        return self.name
