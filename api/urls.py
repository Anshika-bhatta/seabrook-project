from rest_framework.routers import DefaultRouter

from .views import LandingPageViewSet
from geo.views import LocationViewSet
from bookings.views import BookingLinkViewSet
from destinations.views import DestinationViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r"landing-pages", LandingPageViewSet, basename="landing-page")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"booking-links", BookingLinkViewSet, basename="booking-link")
router.register(r"destinations", DestinationViewSet, basename="destination")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = router.urls
