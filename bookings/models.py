from django.db import models

from destinations.models import Destination


class BookingLink(models.Model):
    GOOGLE_FLIGHTS = "google_flights"
    BOOKING_COM = "booking_com"
    SKYSCANNER = "skyscanner"
    EXPEDIA = "expedia"
    OTHER = "other"

    PROVIDER_CHOICES = [
        (
            GOOGLE_FLIGHTS,
            "Google Flights"
        ),
        (
            BOOKING_COM,
            "Booking.com"
        ),
        (
            SKYSCANNER,
            "Skyscanner"
        ),
        (
            EXPEDIA,
            "Expedia"
        ),
        (
            OTHER,
            "Other"
        ),
    ]

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="booking_links"
    )

    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES
    )

    label = models.CharField(
        max_length=100,
        blank=True,
        help_text=(
            "Optional button label, "
            "for example: Book Hotel"
        )
    )

    booking_url = models.URLField(
        max_length=500
    )

    is_active = models.BooleanField(
        default=True
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
            "provider",
        ]

    def __str__(self):
        return (
            f"{self.get_provider_display()} "
            f"- {self.destination.name}"
        )
        