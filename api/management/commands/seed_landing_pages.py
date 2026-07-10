from django.core.management.base import BaseCommand

from destinations.models import Destination
from api.models import LandingPage


LANDING_PAGES = [
    {
        "destination_slug": "seabrook-beach",
        "title": "Plan Your Trip to Seabrook Beach, Texas",
        "slug": "seabrook-beach-travel-guide",
        "h1_heading": "Everything You Need to Know Before Visiting Seabrook Beach",
        "meta_description": (
            "A practical travel guide to Seabrook Beach, Texas — when to go, "
            "how to get there, and what to expect from this Galveston Bay "
            "waterfront town."
        ),
        "meta_keywords": "Seabrook Texas, Seabrook Beach, Galveston Bay travel",
        "content": (
            "Seabrook sits on the western shore of Galveston Bay, roughly "
            "30 minutes from downtown Houston and a short drive from "
            "Houston's two major airports. It's best known as a boating "
            "and waterfront dining town, with a laid-back pace that makes "
            "it an easy day trip or weekend base for exploring the wider "
            "bay area.\n\n"
            "The closest major airport is George Bush Intercontinental "
            "(IAH) or William P. Hobby (HOU), both roughly 40-50 minutes "
            "away by car depending on traffic. From either airport, most "
            "visitors rent a car, since public transit options directly "
            "into Seabrook are limited.\n\n"
            "Most visitors spend their time along the waterfront, with "
            "easy access to nearby Kemah Boardwalk for entertainment, "
            "Galveston Island for beach time, and Space Center Houston for "
            "a half-day trip inland. Seabrook itself works well as a "
            "quieter home base while you explore the surrounding bay area."
        ),
        "canonical_url": "",
        "is_published": True,
    },
    {
        "destination_slug": "kemah-boardwalk",
        "title": "Kemah Boardwalk Visitor Guide",
        "slug": "kemah-boardwalk-visitor-guide",
        "h1_heading": "Planning a Day at Kemah Boardwalk",
        "meta_description": (
            "What to expect at Kemah Boardwalk — rides, restaurants, "
            "parking, and tips for visiting this Galveston Bay waterfront "
            "entertainment district."
        ),
        "meta_keywords": "Kemah Boardwalk, Kemah Texas, Galveston Bay attractions",
        "content": (
            "Kemah Boardwalk is a waterfront entertainment district on "
            "Galveston Bay, roughly five minutes from Seabrook by car. "
            "It's built around a mix of amusement rides, restaurants, and "
            "boutique shops, all connected by a boardwalk that runs along "
            "the marina.\n\n"
            "Most visitors plan for at least half a day here, longer if "
            "traveling with kids interested in the rides. Weekday "
            "mornings and early afternoons tend to be quieter than "
            "weekend evenings, when the boardwalk gets busy with dinner "
            "crowds and live entertainment.\n\n"
            "Parking is available on-site, though weekend lots can fill "
            "up during peak season — arriving before midday is the "
            "easiest way to avoid a wait. Kemah pairs naturally with a "
            "Seabrook home base, since the two are close enough for an "
            "easy evening visit without needing to relocate."
        ),
        "canonical_url": "",
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "Seeds example LandingPage content tied to existing destinations."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for entry in LANDING_PAGES:
            try:
                destination = Destination.objects.get(
                    slug=entry["destination_slug"]
                )
            except Destination.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping '{entry['slug']}' — destination "
                        f"'{entry['destination_slug']}' not found. "
                        f"Run seed_destinations first."
                    )
                )
                continue

            _, created = LandingPage.objects.get_or_create(
                destination=destination,
                defaults={
                    "title": entry["title"],
                    "slug": entry["slug"],
                    "h1_heading": entry["h1_heading"],
                    "content": entry["content"],
                    "meta_description": entry["meta_description"],
                    "meta_keywords": entry["meta_keywords"],
                    "canonical_url": entry["canonical_url"],
                    "is_published": entry["is_published"],
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created landing page: {entry['title']}")
                )
            else:
                skipped_count += 1
                self.stdout.write(f"Skipped (already exists): {entry['title']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Created {created_count}, skipped {skipped_count} "
                f"(already existed)."
            )
        )