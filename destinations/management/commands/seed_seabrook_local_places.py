from django.core.management.base import BaseCommand

from geo.models import Location
from destinations.models import Category, Destination


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
    },
]


class Command(BaseCommand):
    help = (
        "Renames the Beach category to Beaches & Parks, adds Marinas and "
        "Dining categories, and seeds local Seabrook POIs from the real site."
    )

    def handle(self, *args, **options):
        # Idempotent rename: only attempt it if the target name doesn't
        # already exist. This avoids a collision if seed_destinations (which
        # runs first, every deploy) ever recreates a stray "Beach" row from
        # its own hardcoded data before this command gets a chance to run.
        if Category.objects.filter(name="Beaches & Parks").exists():
            self.stdout.write("Category 'Beaches & Parks' already exists, skipping rename")
            # Clean up any stray duplicate "Beach" row left behind by
            # seed_destinations recreating it against the old slug.
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

        marinas_cat, created = Category.objects.get_or_create(
            slug="marinas",
            defaults={"name": "Marinas", "icon": "anchor"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created category: Marinas"))

        dining_cat, created = Category.objects.get_or_create(
            slug="dining",
            defaults={"name": "Dining", "icon": "utensils"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created category: Dining"))

        try:
            seabrook_location = Location.objects.get(
                city="Seabrook", state="Texas", country="United States"
            )
        except Location.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    "No Location found for Seabrook, Texas. Create it in the "
                    "admin first (or run seed_destinations, which creates it "
                    "via the Seabrook Beach entry)."
                )
            )
            return

        created_count = 0
        skipped_count = 0

        for place in LOCAL_PLACES:
            category = Category.objects.get(slug=place["category_slug"])

            _, created = Destination.objects.get_or_create(
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

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created destination: {place['name']}")
                )
            else:
                skipped_count += 1
                self.stdout.write(f"Skipped (already exists): {place['name']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Created {created_count}, skipped {skipped_count} "
                f"(already existed)."
            )
        )