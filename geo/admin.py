from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "state",
        "country",
        "airport_code",
        "created_at",
    )

    search_fields = (
        "city",
        "state",
        "country",
        "airport_code",
    )

    list_filter = (
        "country",
        "state",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "country",
        "city",
    )