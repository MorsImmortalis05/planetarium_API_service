from django.urls import path, include
from rest_framework import routers

from planetarium.views import PlanetariumDomeViewSet, ShowThemeViewSet, \
    AstronomyShowViewSet, ReservationViewSet, ShowSessionViewSet, TicketViewSet

router = routers.DefaultRouter
router.register(prefix="planetarium_domes", viewset=PlanetariumDomeViewSet)
router.register(prefix="show_themes", viewset=ShowThemeViewSet)
router.register(prefix="astronomy_shows", viewset=AstronomyShowViewSet)
router.register(prefix="reservations", viewset=ReservationViewSet)
router.register(prefix="show_sessions", viewset=ShowSessionViewSet)
router.register(prefix="Tickets", viewset=TicketViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "cinema"
