from rest_framework import viewsets
from .models import Location
from .serializers import LocationSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_fields = ["country", "state", "city"]
    search_fields = ["city", "state", "country", "airport_code"]
    ordering_fields = ["country", "city"]