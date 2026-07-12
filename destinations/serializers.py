from rest_framework import serializers
from geo.serializers import LocationSerializer
from bookings.serializers import BookingLinkSerializer
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
    amenities = AmenitySerializer(many=True, read_only=True)
    booking_links = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "description", "category", "location",
            "latitude", "longitude", "address", "image", "is_featured",
            "opening_hours", "amenities", "booking_links",
        ]

    def get_booking_links(self, obj):
        links = obj.booking_links.filter(is_active=True).order_by(
            "display_order"
        )
        return BookingLinkSerializer(links, many=True).data


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
            "opening_hours", "is_featured", "is_active",
            "created_at", "updated_at",
        ]