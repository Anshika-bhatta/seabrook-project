from rest_framework import serializers

from destinations.models import Destination
from .models import LandingPage


class LandingPageDestinationSerializer(serializers.ModelSerializer):
    """Lightweight destination info to nest inside a landing page."""
    class Meta:
        model = Destination
        fields = ["id", "name", "slug", "latitude", "longitude", "address"]


class LandingPageSerializer(serializers.ModelSerializer):
    destination = LandingPageDestinationSerializer(read_only=True)

    class Meta:
        model = LandingPage
        fields = [
            "id",
            "destination",
            "title",
            "slug",
            "h1_heading",
            "content",
            "meta_description",
            "meta_keywords",
            "canonical_url",
            "created_at",
            "updated_at",
        ]
        
