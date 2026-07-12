from django.contrib import admin

from .models import (
    Amenity,
    Category,
    Destination,
    DestinationImage,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        )
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "icon",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage

    extra = 1

    fields = (
        "image",
        "caption",
        "alt_text",
        "is_primary",
        "display_order",
    )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "location",
        "is_featured",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "address",
        "location__city",
        "location__state",
        "location__country",
        "category__name",
    )

    list_filter = (
        "category",
        "is_featured",
        "is_active",
        "location__country",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        )
    }

    filter_horizontal = (
        "amenities",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        DestinationImageInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "category",
                    "location",
                )
            },
        ),
        (
            "Location Details",
            {
                "fields": (
                    "address",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            "Media and Website",
            {
                "fields": (
                    "image",
                    "website",
                    "opening_hours",
                )
            },
        ),
        (
            "Amenities",
            {
                "fields": (
                    "amenities",
                )
            },
        ),
        (
            "Visibility",
            {
                "fields": (
                    "is_featured",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = (
        "destination",
        "display_order",
        "is_primary",
        "created_at",
    )

    search_fields = (
        "destination__name",
        "caption",
        "alt_text",
    )

    list_filter = (
        "is_primary",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "destination",
        "display_order",
    )