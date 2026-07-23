import uuid

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

    opening_hours = models.CharField(
        max_length=150,
        blank=True,
        help_text=(
            "Free-text display hours, e.g. '11:00 AM - 10:00 PM' "
            "or 'Open 24 hours' or 'Varies by season'"
        )
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    is_owner_submitted = models.BooleanField(
        default=False,
        help_text=(
            "True when this listing came in through the public "
            "business self-registration form, rather than being "
            "added by staff via the admin."
        )
    )

    owner_name = models.CharField(
        max_length=150,
        blank=True
    )

    owner_email = models.EmailField(
        blank=True
    )

    owner_phone = models.CharField(
        max_length=30,
        blank=True
    )

    edit_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=(
            "Private token that lets the owner edit this listing without "
            "an account. Never shown publicly - only returned once, at "
            "registration time."
        )
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
