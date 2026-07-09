import django_filters

from .models import Destination


class DestinationFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr="iexact",
    )

    class Meta:
        model = Destination
        fields = ["category", "is_featured", "is_active"]
        