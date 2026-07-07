from django.contrib import admin

from .models import BookingLink


@admin.register(BookingLink)
class BookingLinkAdmin(admin.ModelAdmin):
    list_display = (
        "destination",
        "provider",
        "label",
        "is_active",
        "display_order",
    )

    search_fields = (
        "destination__name",
        "label",
        "booking_url",
    )

    list_filter = (
        "provider",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "display_order",
        "provider",
    )