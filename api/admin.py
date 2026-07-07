from django.contrib import admin

from .models import LandingPage


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "slug",
        "is_published",
        "updated_at",
    )

    search_fields = (
        "title",
        "slug",
        "h1_heading",
        "destination__name",
    )

    list_filter = (
        "is_published",
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": (
            "title",
        )
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Page Information",
            {
                "fields": (
                    "destination",
                    "title",
                    "slug",
                    "h1_heading",
                    "content",
                )
            },
        ),
        (
            "SEO Metadata",
            {
                "fields": (
                    "meta_description",
                    "meta_keywords",
                    "canonical_url",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "is_published",
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