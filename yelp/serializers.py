# api/serializers.py

from rest_framework import serializers
from .models import YelpReview


class YelpReviewSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = YelpReview
        fields = ('review_id', 
                  'user_id', 
                  'stars', 
                  'datetime', 
                  'date', 
                  'time', 
                  'text', 
                  'timestamp')
        read_only_fields = ['timestamp']