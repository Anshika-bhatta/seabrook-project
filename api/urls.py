from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LandingPageViewSet
from geo.views import LocationViewSet
from bookings.views import BookingLinkViewSet
from destinations.views import (
    DestinationViewSet,
    DestinationRegisterView,
    DestinationEditView,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r"landing-pages", LandingPageViewSet, basename="landing-page")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"booking-links", BookingLinkViewSet, basename="booking-link")
router.register(r"destinations", DestinationViewSet, basename="destination")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    # Must come BEFORE router.urls: the router's detail route is
    # destinations/<slug>/, and "register"/"edit" would otherwise be
    # swallowed by that pattern and treated as a slug lookup.
    path(
        "destinations/register/",
        DestinationRegisterView.as_view(),
        name="destination-register",
    ),
    path(
        "destinations/edit/<uuid:edit_token>/",
        DestinationEditView.as_view(),
        name="destination-edit",
    ),
] + router.urls
