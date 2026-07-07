from rest_framework import viewsets
from .models import Destination, Category
from .serializers import (
    DestinationListSerializer,
    DestinationDetailSerializer,
    CategorySerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filterset_fields = ["category", "is_featured", "is_active"]
    search_fields = ["name", "description", "address"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        return Destination.objects.filter(
            is_active=True
        ).select_related("location", "category").prefetch_related(
            "amenities", "gallery"
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DestinationDetailSerializer
        return DestinationListSerializer