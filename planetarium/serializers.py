from rest_framework import serializers

from planetarium.models import AstronomyShow, PlanetariumDome, Reservation, \
    ShowTheme, ShowSession, Ticket


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name", )


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = ShowThemeSerializer(
        many=True
    )
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "themes", )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", )


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.PrimaryKeyRelatedField(
        queryset=AstronomyShow.objects.all())
    planetarium_dome = serializers.PrimaryKeyRelatedField(
        queryset=PlanetariumDome.objects.all())

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time",
            "tickets_sold"
        )


class TicketSerializer(serializers.ModelSerializer):
    show_session = ShowSessionSerializer(
        read_only=True
    )
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat","show_session")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_theme = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )


class ShowThemeListSerializer(ShowThemeSerializer):
    shows = serializers.SlugRelatedField(
        read_only=True, slug_field="title"
    )
    class Meta:
        model = ShowTheme
        fields = ("id", "name", "shows")
