from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from planetarium.models import PlanetariumDome, ShowTheme, AstronomyShow, \
    Reservation, ShowSession, Ticket
from planetarium.serializers import PlanetariumDomeSerializer, \
    ShowThemeSerializer, AstronomyShowSerializer, ReservationSerializer, \
    ShowSessionSerializer, TicketSerializer


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ShowSessionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer


class TicketViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
