from urllib.parse import quote

from django.core.management.base import BaseCommand

from geo.models import Location
from destinations.models import Category, Destination, Amenity
from bookings.models import BookingLink


AMENITY_DEFAULTS = {
    "Parking": {"icon": "🅿️", "description": "On-site or nearby parking available."},
    "Restrooms": {"icon": "🚻", "description": "Public restrooms available."},
    "Food & Dining": {"icon": "🍽️", "description": "Restaurants or food vendors on site."},
    "Wheelchair Accessible": {"icon": "♿", "description": "Accessible pathways and facilities."},
    "Pet Friendly": {"icon": "🐾", "description": "Pets welcome in outdoor areas."},
    "Gift Shop": {"icon": "🛍️", "description": "On-site gift or souvenir shop."},
    "Hiking Trails": {"icon": "🥾", "description": "Marked trails for walking or hiking."},
    "Fishing": {"icon": "🎣", "description": "Fishing permitted or facilities available."},
}


SEED_DATA = [
    {
        "name": "Kemah Boardwalk",
        "slug": "kemah-boardwalk",
        "category": {"name": "Theme Park", "slug": "theme-park", "icon": "ferris-wheel"},
        "location": {
            "city": "Kemah", "state": "Texas", "country": "United States",
            "latitude": "29.535200", "longitude": "-95.018000", "airport_code": "HOU",
        },
        "latitude": "29.535200",
        "longitude": "-95.018000",
        "address": "215 Kipp Ave, Kemah, TX 77565",
        "description": (
            "A lively waterfront entertainment district on Galveston Bay, "
            "featuring rides, restaurants, and boardwalk shops just minutes "
            "from Seabrook."
        ),
        "amenities": ["Parking", "Restrooms", "Food & Dining", "Wheelchair Accessible"],
    },
    {
        "name": "Galveston Seawall & Beach",
        "slug": "galveston-seawall-beach",
        "category": {"name": "Beach", "slug": "beach", "icon": "beach"},
        "location": {
            "city": "Galveston", "state": "Texas", "country": "United States",
            "latitude": "29.254400", "longitude": "-94.847800", "airport_code": "GLS",
        },
        "latitude": "29.254400",
        "longitude": "-94.847800",
        "address": "Seawall Blvd, Galveston, TX 77550",
        "description": (
            "A ten-mile stretch of seawall and sandy beach along the Gulf "
            "of Mexico, popular for swimming, biking, and Gulf Coast sunsets."
        ),
        "amenities": ["Parking", "Restrooms", "Pet Friendly"],
    },
    {
        "name": "Space Center Houston",
        "slug": "space-center-houston",
        "category": {"name": "Museum", "slug": "museum", "icon": "rocket"},
        "location": {
            "city": "Houston", "state": "Texas", "country": "United States",
            "latitude": "29.551800", "longitude": "-95.098000", "airport_code": "HOU",
        },
        "latitude": "29.551800",
        "longitude": "-95.098000",
        "address": "1601 E NASA Pkwy, Houston, TX 77058",
        "description": (
            "The official visitor center of NASA's Johnson Space Center, "
            "with real spacecraft, astronaut training areas, and interactive "
            "exhibits."
        ),
        "amenities": ["Parking", "Restrooms", "Wheelchair Accessible", "Gift Shop", "Food & Dining"],
    },
    {
        "name": "Moody Gardens",
        "slug": "moody-gardens",
        "category": {"name": "Theme Park", "slug": "theme-park", "icon": "ferris-wheel"},
        "location": {
            "city": "Galveston", "state": "Texas", "country": "United States",
            "latitude": "29.286100", "longitude": "-94.846700", "airport_code": "GLS",
        },
        "latitude": "29.286100",
        "longitude": "-94.846700",
        "address": "1 Hope Blvd, Galveston, TX 77554",
        "description": (
            "A family-friendly campus with a rainforest pyramid, aquarium, "
            "and seasonal light displays set on Galveston Island."
        ),
        "amenities": ["Parking", "Restrooms", "Food & Dining", "Wheelchair Accessible", "Gift Shop"],
    },
    {
        "name": "Armand Bayou Nature Center",
        "slug": "armand-bayou-nature-center",
        "category": {"name": "Nature", "slug": "nature", "icon": "leaf"},
        "location": {
            "city": "Pasadena", "state": "Texas", "country": "United States",
            "latitude": "29.582700", "longitude": "-95.098300", "airport_code": "HOU",
        },
        "latitude": "29.582700",
        "longitude": "-95.098300",
        "address": "8500 Bay Area Blvd, Pasadena, TX 77507",
        "description": (
            "One of the largest urban wilderness preserves in the U.S., "
            "with hiking trails through marsh, prairie, and forest habitats."
        ),
        "amenities": ["Parking", "Restrooms", "Hiking Trails"],
    },
    {
        "name": "San Jacinto Monument & Battleground",
        "slug": "san-jacinto-monument-battleground",
        "category": {"name": "Historic Site", "slug": "historic-site", "icon": "monument"},
        "location": {
            "city": "La Porte", "state": "Texas", "country": "United States",
            "latitude": "29.753000", "longitude": "-95.081900", "airport_code": "HOU",
        },
        "latitude": "29.753000",
        "longitude": "-95.081900",
        "address": "1 Monument Cir, La Porte, TX 77571",
        "description": (
            "A 567-foot monument and museum marking the site of the "
            "decisive 1836 battle for Texas independence, with a "
            "observation deck overlooking the Houston Ship Channel."
        ),
        "amenities": ["Parking", "Restrooms", "Wheelchair Accessible", "Gift Shop"],
    },
    {
        "name": "Seawolf Park",
        "slug": "seawolf-park",
        "category": {"name": "Nature", "slug": "nature", "icon": "leaf"},
        "location": {
            "city": "Galveston", "state": "Texas", "country": "United States",
            "latitude": "29.311600", "longitude": "-94.796300", "airport_code": "GLS",
        },
        "latitude": "29.311600",
        "longitude": "-94.796300",
        "address": "100 Seawolf Park Blvd, Galveston, TX 77550",
        "description": (
            "A waterfront park on Pelican Island featuring a decommissioned "
            "WWII submarine and destroyer escort open for tours, plus "
            "fishing piers and bay views."
        ),
        "amenities": ["Parking", "Restrooms", "Fishing"],
    },
    {
        "name": "Texas City Dike",
        "slug": "texas-city-dike",
        "category": {"name": "Beach", "slug": "beach", "icon": "beach"},
        "location": {
            "city": "Texas City", "state": "Texas", "country": "United States",
            "latitude": "29.417700", "longitude": "-94.875200", "airport_code": "HOU",
        },
        "latitude": "29.417700",
        "longitude": "-94.875200",
        "address": "Skyline Dr, Texas City, TX 77590",
        "description": (
            "A five-mile stretch extending into Galveston Bay, popular for "
            "fishing, crabbing, and watching ships pass through the "
            "Houston Ship Channel."
        ),
        "amenities": ["Parking", "Fishing", "Pet Friendly"],
    },
]


class Command(BaseCommand):
    help = "Seeds Location, Category, and Destination records for the Seabrook area."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for entry in SEED_DATA:
            loc_data = entry["location"]
            location, loc_created = Location.objects.get_or_create(
                country=loc_data["country"],
                state=loc_data["state"],
                city=loc_data["city"],
                defaults={
                    "latitude": loc_data["latitude"],
                    "longitude": loc_data["longitude"],
                    "airport_code": loc_data["airport_code"],
                },
            )

            cat_data = entry["category"]
            category, cat_created = Category.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={
                    "name": cat_data["name"],
                    "icon": cat_data["icon"],
                },
            )

            destination, dest_created = Destination.objects.get_or_create(
                slug=entry["slug"],
                defaults={
                    "location": location,
                    "category": category,
                    "name": entry["name"],
                    "description": entry["description"],
                    "latitude": entry["latitude"],
                    "longitude": entry["longitude"],
                    "address": entry["address"],
                    "is_active": True,
                },
            )

            amenity_objs = []
            for amenity_name in entry.get("amenities", []):
                defaults = AMENITY_DEFAULTS.get(amenity_name, {})
                amenity, _ = Amenity.objects.get_or_create(
                    name=amenity_name,
                    defaults=defaults,
                )
                amenity_objs.append(amenity)

            if amenity_objs:
                destination.amenities.set(amenity_objs)

            city_query = quote(f"{loc_data['city']}, {loc_data['state']}")
            airport = loc_data["airport_code"]

            booking_link_specs = [
                {
                    "provider": BookingLink.GOOGLE_FLIGHTS,
                    "label": "Book Flight",
                    "booking_url": (
                        f"https://www.google.com/travel/flights?q=Flights+to+{airport}"
                        if airport
                        else "https://www.google.com/travel/flights"
                    ),
                    "display_order": 0,
                },
                {
                    "provider": BookingLink.BOOKING_COM,
                    "label": "Find Hotels Nearby",
                    "booking_url": (
                        f"https://www.booking.com/searchresults.html?ss={city_query}"
                    ),
                    "display_order": 1,
                },
            ]

            for spec in booking_link_specs:
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

            if dest_created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created destination: {entry['name']}")
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    f"Skipped (already exists): {entry['name']}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Created {created_count}, skipped {skipped_count} "
                f"(already existed)."
            )
        )