from rest_framework import serializers

from planetarium.models import AstronomyShow, PlanetariumDome, Reservation, \
    ShowTheme, ShowSession, Ticket


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("name", "rows", "seats_in_row")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("name", )


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = ShowThemeSerializer(
        many=True
    )
    class Meta:
        model = AstronomyShow
        fields = ("title", "description", "themes", )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("created_at", )


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        read_only=True, slug_field="title"
    )
    planetarium_dome = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    class Meta:
        model = ShowSession
        fields = ("astronomy_show", "planetarium_dome", "show_time")



class TicketSerializer(serializers.ModelSerializer):
    show_session = ShowSessionSerializer(
        read_only=True
    )
    class Meta:
        model = Ticket
        fields = ("row", "seat","show_session")


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
        fields = ("name", "shows")
