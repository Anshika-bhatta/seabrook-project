from django.db import models

from destinations.models import Destination


class LandingPage(models.Model):
    destination = models.OneToOneField(
        Destination,
        on_delete=models.CASCADE,
        related_name="landing_page"
    )

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        max_length=255,
        unique=True
    )

    meta_description = models.CharField(
        max_length=320
    )

    meta_keywords = models.TextField(
        blank=True
    )

    h1_heading = models.CharField(
        max_length=255
    )

    content = models.TextField()

    canonical_url = models.URLField(
        blank=True
    )

    is_published = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["title"]

        indexes = [
            models.Index(
                fields=["slug"]
            ),
            models.Index(
                fields=["is_published"]
            ),
        ]

    def __str__(self):
        return self.title
    