from django.db import models

from geo.models import Location


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=120,
        unique=True
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text=(
            "Optional icon name, for example: "
            "beach, hotel, restaurant"
        )
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

        verbose_name = "Category"

        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    icon = models.CharField(
        max_length=50,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

        verbose_name = "Amenity"

        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class Destination(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="destinations"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="destinations"
    )

    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name="destinations"
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        max_length=220,
        unique=True
    )

    description = models.TextField()

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    address = models.CharField(
        max_length=255
    )

    image = models.ImageField(
        upload_to="destinations/",
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(
                fields=["slug"]
            ),
            models.Index(
                fields=["is_featured"]
            ),
            models.Index(
                fields=["is_active"]
            ),
        ]

    def __str__(self):
        return self.name


class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="destination_gallery/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alternative text for accessibility and SEO"
    )

    is_primary = models.BooleanField(
        default=False
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "display_order",
            "id",
        ]

    def __str__(self):
        return (
            f"{self.destination.name} "
            f"- Image {self.id}"
        )
        
