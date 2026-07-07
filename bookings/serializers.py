from rest_framework import serializers
from .models import BookingLink


class BookingLinkSerializer(serializers.ModelSerializer):
    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )

    class Meta:
        model = BookingLink
        fields = [
            "id", "destination", "provider", "provider_display",
            "label", "booking_url", "is_active", "display_order",
        ]