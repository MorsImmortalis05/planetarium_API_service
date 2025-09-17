from django.urls import path, include
from rest_framework import routers

from planetarium.views import PlanetariumDomeViewSet, ShowThemeViewSet, \
    AstronomyShowViewSet, ReservationViewSet, ShowSessionViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register("domes", viewset=PlanetariumDomeViewSet)
router.register(prefix="themes", viewset=ShowThemeViewSet)
router.register(prefix="shows", viewset=AstronomyShowViewSet)
router.register(prefix="reservations", viewset=ReservationViewSet)
router.register(prefix="sessions", viewset=ShowSessionViewSet)
router.register(prefix="tickets", viewset=TicketViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
