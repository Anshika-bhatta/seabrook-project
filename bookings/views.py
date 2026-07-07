from rest_framework import viewsets
from .models import BookingLink
from .serializers import BookingLinkSerializer


class BookingLinkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookingLinkSerializer
    filterset_fields = ["destination", "provider", "is_active"]
    ordering_fields = ["display_order", "provider"]

    def get_queryset(self):
        return BookingLink.objects.filter(
            is_active=True
        ).select_related("destination")