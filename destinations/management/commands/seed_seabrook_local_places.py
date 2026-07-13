from urllib.parse import quote

from django.core.management.base import BaseCommand

from geo.models import Location
from destinations.models import Category, Destination, Amenity
from bookings.models import BookingLink


AMENITY_DEFAULTS = {
    "Parking": {"icon": "🅿️", "description": "On-site or nearby parking available."},
    "Restrooms": {"icon": "🚻", "description": "Public restrooms available."},
    "Fishing": {"icon": "🎣", "description": "Fishing permitted or facilities available."},
    "Food & Dining": {"icon": "🍽️", "description": "Restaurants or food vendors on site."},
}

LOCAL_PLACES = [
    {
        "name": "Pine Gully Park & Pier",
        "slug": "pine-gully-park-pier",
        "category_slug": "beaches-parks",
        "latitude": "29.584700",
        "longitude": "-95.016500",
        "description": (
            "A 52-acre bayfront park with a fishing pier, boardwalks, and "
            "some of the best birding on Galveston Bay."
        ),
        "amenities": ["Parking", "Restrooms", "Fishing"],
        "opening_hours": "6:00 AM - 10:00 PM",
    },
    {
        "name": "Meador Park",
        "slug": "meador-park",
        "category_slug": "beaches-parks",
        "latitude": "29.577200",
        "longitude": "-95.023100",
        "description": (
            "A family park with a splash pad, playground, and shaded "
            "picnic areas."
        ),
        "amenities": ["Parking", "Restrooms"],
        "opening_hours": "6:00 AM - 10:00 PM",
    },
    {
        "name": "Miramar Park",
        "slug": "miramar-park",
        "category_slug": "beaches-parks",
        "latitude": "29.573500",
        "longitude": "-95.019800",
        "description": (
            "A waterfront park with bay access, walking paths, and sunset "
            "views."
        ),
        "amenities": ["Parking", "Restrooms"],
        "opening_hours": "6:00 AM - 10:00 PM",
    },
    {
        "name": "Seabrook Sailing Club",
        "slug": "seabrook-sailing-club",
        "category_slug": "marinas",
        "latitude": "29.563600",
        "longitude": "-95.021700",
        "description": (
            "A Clear Lake sailing club known for regattas and youth "
            "sailing programs."
        ),
        "amenities": ["Parking", "Restrooms"],
        "opening_hours": "Open 24 hours",
    },
    {
        "name": "Endeavour Marina",
        "slug": "endeavour-marina",
        "category_slug": "marinas",
        "latitude": "29.565200",
        "longitude": "-95.020000",
        "description": (
            "A full-service marina with wet slips and dry storage near "
            "the Kemah bridge."
        ),
        "amenities": ["Parking", "Restrooms"],
        "opening_hours": "Open 24 hours",
    },
    {
        "name": "Seabrook Marina",
        "slug": "seabrook-marina-local",
        "category_slug": "marinas",
        "latitude": "29.558300",
        "longitude": "-95.025000",
        "description": (
            "A sheltered marina with deep-water access straight out to "
            "Galveston Bay."
        ),
        "amenities": ["Parking", "Restrooms", "Fishing"],
        "opening_hours": "Open 24 hours",
    },
    {
        "name": "Pelican Grill",
        "slug": "pelican-grill",
        "category_slug": "dining",
        "latitude": "29.571000",
        "longitude": "-95.018000",
        "description": (
            "A waterfront restaurant serving fresh Gulf seafood with "
            "marina views."
        ),
        "amenities": ["Parking", "Food & Dining"],
        "opening_hours": "11:00 AM - 9:00 PM",
    },
    {
        "name": "Tookie's Seafood",
        "slug": "tookies-seafood",
        "category_slug": "dining",
        "latitude": "29.564500",
        "longitude": "-95.022800",
        "description": (
            "A local seafood favorite praised for its fresh catch and "
            "classic Gulf plates."
        ),
        "amenities": ["Parking", "Food & Dining"],
        "opening_hours": "11:00 AM - 9:00 PM",
    },
]

SEABROOK_BEACH_EXTRAS = {
    "slug": "seabrook-beach",
    "amenities": ["Parking", "Restrooms"],
    "opening_hours": "Open 24 hours",
}


def apply_booking_links(destination, city, state, airport_code=""):
    city_query = quote(f"{city}, {state}")
    specs = [
        {
            "provider": BookingLink.GOOGLE_FLIGHTS,
            "label": "Book Flight",
            "booking_url": (
                f"https://www.google.com/travel/flights?q=Flights+to+{airport_code}"
                if airport_code
                else "https://www.google.com/travel/flights"
            ),
            "display_order": 0,
        },
        {
            "provider": BookingLink.BOOKING_COM,
            "label": "Find Hotels Nearby",
            "booking_url": f"https://www.booking.com/searchresults.html?ss={city_query}",
            "display_order": 1,
        },
    ]
    for spec in specs:
        BookingLink.objects.get_or_create(
            destination=destination,
            provider=spec["provider"],
            label=spec["label"],
            defaults={
                "booking_url": spec["booking_url"],
                "is_active": True,
                "display_order": spec["display_order"],
            },
        )


def apply_amenities(destination, amenity_names):
    amenity_objs = []
    for name in amenity_names:
        defaults = AMENITY_DEFAULTS.get(name, {})
        amenity, _ = Amenity.objects.get_or_create(name=name, defaults=defaults)
        amenity_objs.append(amenity)
    if amenity_objs:
        destination.amenities.set(amenity_objs)


class Command(BaseCommand):
    help = (
        "Renames the Beach category to Beaches & Parks, adds Marinas and "
        "Dining categories, and seeds local Seabrook POIs with amenities, "
        "hours, and booking links."
    )

    def handle(self, *args, **options):
        if Category.objects.filter(name="Beaches & Parks").exists():
            self.stdout.write("Category 'Beaches & Parks' already exists, skipping rename")
            Category.objects.filter(slug="beach").exclude(
                name="Beaches & Parks"
            ).delete()
        else:
            renamed = Category.objects.filter(slug="beach").update(
                name="Beaches & Parks", slug="beaches-parks"
            )
            if renamed:
                self.stdout.write(
                    self.style.SUCCESS("Renamed 'Beach' category to 'Beaches & Parks'")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "No 'beach' category found to rename — creating "
                        "'Beaches & Parks' fresh."
                    )
                )
                Category.objects.get_or_create(
                    slug="beaches-parks",
                    defaults={"name": "Beaches & Parks", "icon": "beach"},
                )

        Category.objects.get_or_create(
            slug="marinas", defaults={"name": "Marinas", "icon": "anchor"}
        )
        Category.objects.get_or_create(
            slug="dining", defaults={"name": "Dining", "icon": "utensils"}
        )

        try:
            seabrook_location = Location.objects.get(
                city="Seabrook", state="Texas", country="United States"
            )
        except Location.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    "No Location found for Seabrook, Texas. Run "
                    "seed_destinations first."
                )
            )
            return

        created_count = 0
        skipped_count = 0

        for place in LOCAL_PLACES:
            category = Category.objects.get(slug=place["category_slug"])

            destination, created = Destination.objects.get_or_create(
                slug=place["slug"],
                defaults={
                    "location": seabrook_location,
                    "category": category,
                    "name": place["name"],
                    "description": place["description"],
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "address": "Seabrook, TX",
                    "is_active": True,
                },
            )

            desired_hours = place.get("opening_hours", "")
            if destination.opening_hours != desired_hours:
                destination.opening_hours = desired_hours
                destination.save(update_fields=["opening_hours"])

            apply_amenities(destination, place.get("amenities", []))
            apply_booking_links(destination, "Seabrook", "Texas", "HOU")

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created destination: {place['name']}")
                )
            else:
                skipped_count += 1
                self.stdout.write(f"Synced data for: {place['name']}")

        try:
            seabrook_beach = Destination.objects.get(
                slug=SEABROOK_BEACH_EXTRAS["slug"]
            )
            desired_hours = SEABROOK_BEACH_EXTRAS["opening_hours"]
            if seabrook_beach.opening_hours != desired_hours:
                seabrook_beach.opening_hours = desired_hours
                seabrook_beach.save(update_fields=["opening_hours"])
            apply_amenities(seabrook_beach, SEABROOK_BEACH_EXTRAS["amenities"])
            apply_booking_links(seabrook_beach, "Seabrook", "Texas", "HOU")
            self.stdout.write(
                self.style.SUCCESS("Synced amenities/hours/booking for Seabrook Beach")
            )
        except Destination.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(
                    "No 'seabrook-beach' destination found — skipping patch."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Created {created_count}, synced {skipped_count} "
                f"existing local places."
            )
        )
