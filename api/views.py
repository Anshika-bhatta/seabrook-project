from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from .models import LandingPage
from .serializers import LandingPageSerializer


@api_view(['GET'])
def home(request):
    return Response({
        "message": "Backend is working!"
    })


class LandingPageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LandingPageSerializer
    lookup_field = "slug"
    search_fields = ["title", "h1_heading", "meta_keywords"]
    ordering_fields = ["title", "created_at", "updated_at"]

    def get_queryset(self):
        return LandingPage.objects.filter(
            is_published=True
        ).select_related("destination")