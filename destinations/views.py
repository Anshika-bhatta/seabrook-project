from rest_framework import viewsets, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Destination, Category
from .serializers import (
    DestinationListSerializer,
    DestinationDetailSerializer,
    DestinationRegisterSerializer,
    CategorySerializer,
)
from .filters import DestinationFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filterset_class = DestinationFilter
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


class DestinationRegisterView(generics.CreateAPIView):
    """
    POST-only public endpoint for the business self-registration form.
    Anyone can submit (no auth) - accepts multipart/form-data so the
    photo upload comes through in the same request as the rest of the
    fields. Listings go live immediately (see DestinationRegisterSerializer).
    """

    queryset = Destination.objects.all()
    serializer_class = DestinationRegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]
