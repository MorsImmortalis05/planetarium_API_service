from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from planetarium.models import PlanetariumDome, ShowTheme, AstronomyShow, \
    Reservation, ShowSession, Ticket
from planetarium.permissions import \
    IsAdminUpdateCreateOrIfAuthenticatedReadOnly, \
    IsAdminOrAuthenticatedReadOnly, IsOwnerOrAdmin
from planetarium.serializers import PlanetariumDomeSerializer, \
    ShowThemeSerializer, AstronomyShowSerializer, ReservationSerializer, \
    ShowSessionSerializer, TicketSerializer


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminUpdateCreateOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = PlanetariumDome.objects.all()

        if name:
            queryset = queryset.filter(title__icontains=name)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter domes by name (partial match)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminUpdateCreateOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = ShowTheme.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter show themes by name (partial match)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AstronomyShowViewSet(ModelViewSet):
    serializer_class = AstronomyShowSerializer
    queryset = AstronomyShow.objects.all()
    permission_classes = (IsAdminOrAuthenticatedReadOnly, )

    def get_queryset(self):
        title = self.request.query_params.get("title")
        themes = self.request.query_params.get("themes")
        queryset = AstronomyShow.objects.all()

        if self.action in ("list", "retrieve"):
            queryset = AstronomyShow.objects.prefetch_related("themes")

        if themes:
            themes_ids = [int(str_id) for str_id in themes.split(",")]
            queryset = queryset.filter(themes__id__in=themes_ids)

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Filter shows by title (partial match)",
                required=False,
            ),
            OpenApiParameter(
                "themes",
                type={"type": "list", "items": {"type": "number"}},
                description="Comma-separated list of theme IDs"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsOwnerOrAdmin, )

    def get_queryset(self):
        user_id = self.request.query_params.get("user")
        queryset = Reservation.objects.all()

        if user_id:
            queryset = queryset.filter(user_id__exact=user_id)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user_id",
                type={"type": "array", "items": {"type": "integer"}},
                location=OpenApiParameter.QUERY,
                description="Filter reservations by user id",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ShowSessionViewSet(ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get_queryset(self):
        astronomy_shows = self.request.query_params.get("astronomy_shows")
        planetarium_domes = self.request.query_params.get("planetarium_domes")
        queryset = ShowSession.objects.all()

        if self.action in ("list", "retrieve"):
            queryset = ShowSession.objects.select_related(
                "astronomy_show",
                "planetarium_dome"
            )

        if astronomy_shows:
            astronomy_shows_ids = [
                int(str_id) for str_id in astronomy_shows.split(",")]
            queryset = queryset.filter(astronomy_show__id__in=astronomy_shows_ids)

        if planetarium_domes:
            planetarium_domes_ids = [
                int(str_id) for str_id in planetarium_domes.split(",")]
            queryset = queryset.filter(planetarium_dome_id__in=planetarium_domes_ids)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "astronomy_shows",
                type={"type": "array", "items": {"type": "integer"}},
                location=OpenApiParameter.QUERY,
                description="Filter show sessions by shows ids",
                required=False,
            ),
            OpenApiParameter(
                "planetarium_domes",
                type={"type": "array", "items": {"type": "integer"}},
                location=OpenApiParameter.QUERY,
                description="Filter show sessions by domes ids"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TicketViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        show_sessions = self.request.query_params.get("show_sessions")
        queryset = Ticket.objects.all()

        if self.action in ("list", "retrieve"):
            queryset = Ticket.objects.select_related("show_session")

        if show_sessions:
            show_session_ids = [int(sid) for sid in show_sessions.split(",")]
            queryset = queryset.filter(show_session__id__in=show_session_ids)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_sessions",
                type={"type": "array", "items": {"type": "integer"}},
                location=OpenApiParameter.QUERY,
                description="Filter tickets by show session ids",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
