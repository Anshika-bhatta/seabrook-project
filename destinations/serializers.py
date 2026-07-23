from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from geo.models import Location
from geo.serializers import LocationSerializer
from bookings.serializers import BookingLinkSerializer
from .models import Category, Amenity, Destination, DestinationImage

# All self-registered businesses belong to this one fixed town - the form
# never asks the owner to pick a city, it's always Seabrook, TX.
SEABROOK_LOCATION = {
    "country": "United States",
    "state": "Texas",
    "city": "Seabrook",
}
SEABROOK_LATLON = (29.5641, -95.0263)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "description"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "icon", "description"]


class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = [
            "id", "image", "caption", "alt_text",
            "is_primary", "display_order",
        ]


class DestinationListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    booking_links = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "description", "category", "location",
            "latitude", "longitude", "address", "image", "is_featured",
            "opening_hours", "amenities", "booking_links",
        ]

    def get_booking_links(self, obj):
        links = obj.booking_links.filter(is_active=True).order_by(
            "display_order"
        )
        return BookingLinkSerializer(links, many=True).data


class DestinationDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    gallery = DestinationImageSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "description",
            "category", "location", "amenities", "gallery",
            "latitude", "longitude", "address", "image", "website",
            "opening_hours", "is_featured", "is_active",
            "created_at", "updated_at",
        ]


class DestinationRegisterSerializer(serializers.ModelSerializer):
    """
    Public write endpoint for business self-registration. Goes live
    immediately (is_active defaults True on the model) - no admin
    approval gate. Owner contact fields are write-only: they're stored
    for the admin's own records but never exposed by the read endpoints.
    """

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        help_text="Category slug, e.g. 'dining', 'marinas'.",
    )

    amenities = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        write_only=True,
    )

    image = serializers.ImageField(required=False)

    # Honeypot: kept empty and visually hidden on the real form. Bots that
    # fill every field trip this and get rejected before hitting the DB.
    company_website_confirm = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "description", "category",
            "address", "latitude", "longitude", "image", "website",
            "opening_hours", "amenities",
            "owner_name", "owner_email", "owner_phone",
            "company_website_confirm", "edit_token",
        ]
        read_only_fields = ["id", "slug", "edit_token"]
        extra_kwargs = {
            "owner_name": {"write_only": True, "required": True},
            "owner_email": {"write_only": True, "required": True},
            "owner_phone": {"write_only": True, "required": False},
        }

    def validate_company_website_confirm(self, value):
        if value:
            # A real visitor never sees or fills this field.
            raise serializers.ValidationError("Submission rejected.")
        return value

    def create(self, validated_data):
        amenity_names = validated_data.pop("amenities", [])
        validated_data.pop("company_website_confirm", None)

        location, _ = Location.objects.get_or_create(
            **SEABROOK_LOCATION,
            defaults={
                "latitude": SEABROOK_LATLON[0],
                "longitude": SEABROOK_LATLON[1],
            },
        )

        base_slug = slugify(validated_data["name"])[:200] or "listing"
        slug = base_slug
        suffix = 2
        while Destination.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        with transaction.atomic():
            destination = Destination.objects.create(
                location=location,
                slug=slug,
                is_active=True,
                is_owner_submitted=True,
                **validated_data,
            )

            if amenity_names:
                amenities = []
                for raw in amenity_names:
                    name = raw.strip()
                    if not name:
                        continue
                    amenity, _ = Amenity.objects.get_or_create(
                        name__iexact=name,
                        defaults={"name": name},
                    )
                    amenities.append(amenity)
                destination.amenities.set(amenities)

        return destination


class DestinationEditSerializer(serializers.ModelSerializer):
    """
    Lets an owner update their own listing using the private edit_token
    from registration - no accounts, no login. Possession of the token
    (a UUID, effectively unguessable) is the only authorization check.
    Partial updates (PATCH) only touch fields actually sent; image and
    amenities are left untouched if omitted.
    """

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=False,
    )

    amenities = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        write_only=True,
    )

    image = serializers.ImageField(required=False)

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "description", "category",
            "address", "latitude", "longitude", "image", "website",
            "opening_hours", "amenities",
            "owner_name", "owner_email", "owner_phone",
        ]
        read_only_fields = ["id", "slug"]
        extra_kwargs = {
            "owner_name": {"write_only": True},
            "owner_email": {"write_only": True},
            "owner_phone": {"write_only": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # amenities is write_only above (list of plain strings in, for
        # symmetry with the register form) but the edit form still needs
        # the CURRENT amenities to prefill itself, so surface them here.
        data["amenities"] = [a.name for a in instance.amenities.all()]
        return data

    def update(self, instance, validated_data):
        amenity_names = validated_data.pop("amenities", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if amenity_names is not None:
            amenities = []
            for raw in amenity_names:
                name = raw.strip()
                if not name:
                    continue
                amenity, _ = Amenity.objects.get_or_create(
                    name__iexact=name,
                    defaults={"name": name},
                )
                amenities.append(amenity)
            instance.amenities.set(amenities)

        return instance
