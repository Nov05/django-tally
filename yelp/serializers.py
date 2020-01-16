# api/serializers.py

from rest_framework import serializers
from .models import YelpScraping


class YelpScrapingSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = YelpScraping
        fields = ('uuid', 
                  'review_id', 
                  'user_id', 
                  'stars', 
                  'datetime', 
                  'date', 
                  'time', 
                  'text', 
                  'timestamp')
        read_only_fields = ['timestamp']