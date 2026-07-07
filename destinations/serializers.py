from rest_framework import serializers
from geo.serializers import LocationSerializer
from .models import Category, Amenity, Destination, DestinationImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "description"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "icon", "description"]


class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = [
            "id", "image", "caption", "alt_text",
            "is_primary", "display_order",
        ]


class DestinationListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "category", "location",
            "latitude", "longitude", "address", "image", "is_featured",
        ]


class DestinationDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    gallery = DestinationImageSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "description",
            "category", "location", "amenities", "gallery",
            "latitude", "longitude", "address", "image", "website",
            "is_featured", "is_active", "created_at", "updated_at",
        ]