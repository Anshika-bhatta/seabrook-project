from django.db import models

class Location(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    airport_code = models.CharField(
        max_length=10,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["country", "city"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "country",
                    "state",
                    "city",
                ],
                name="unique_location_city"
            )
        ]
        
    def __str__(self):
        return f"{self.city}, {self.country}"