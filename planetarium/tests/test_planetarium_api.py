import tempfile
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    Reservation,
    ShowSession,
    Ticket
)
from planetarium.serializers import (
    PlanetariumDomeSerializer,
    ShowThemeSerializer,
    AstronomyShowSerializer,
    ReservationSerializer,
    ShowSessionSerializer,
    TicketSerializer
)
from user.models import User

PLANETARIUM_DOME_URL = reverse("planetarium:planetariumdome-list")
ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")
SHOW_SESSION_URL = reverse("planetarium:showsession-list")
SHOW_THEME_URL = reverse("planetarium:showtheme-list")
RESERVATION_URL = reverse("planetarium:reservation-list")
TICKET_URL = reverse("planetarium:ticket-list")

def dome_detail_url(dome_id):
    return reverse("planetarium:planetariumdome-detail", args=[dome_id])

def show_detail_url(show_id):
    return reverse("planetarium:astronomyshow-detail", args=[show_id])

def session_detail_url(session_id):
    return reverse("planetarium:showsession-detail", args=[session_id])

def theme_detail_url(theme_id):
    return reverse("planetarium:showtheme-detail", args=[theme_id])

def reservation_detail_url(reservation_id):
    return reverse("planetarium:reservation-detail", args=[reservation_id])

def ticket_detail_url(ticket_id):
    return reverse("planetarium:ticket-detail", args=[ticket_id])

def sample_dome(**params):
    defaults = {
        "name": "Andromeda",
        "rows": 10,
        "seats_in_row": 20
    }
    defaults.update(params)

    return PlanetariumDome.objects.create(**defaults)


def sample_show_theme(**params):
    defaults = {
        "name": "Cosmogony",
    }
    defaults.update(params)

    return ShowTheme.objects.create(**defaults)


def sample_astronomy_show(**params):
    theme = params.pop("themes", sample_show_theme())
    defaults = {
        "title": "Star come back",
        "description": "Very interesting show for kids",
    }
    defaults.update(params)

    show = AstronomyShow.objects.create(**defaults)
    show.themes.set([theme])
    return show


def sample_reservation(**params):
    user = get_user_model().objects.create_user(email="testuser",
                                                password="12345")
    defaults = {
        "user": user
    }
    defaults.update(params)

    return Reservation.objects.create(**defaults)


def sample_show_session(**params):
    astronomy_show = sample_astronomy_show()
    planetarium_dome = sample_dome()
    defaults = {
        "astronomy_show": astronomy_show,
        "planetarium_dome": planetarium_dome,
        "show_time": timezone.now()
    }
    defaults.update(params)

    return ShowSession.objects.create(**defaults)


def sample_ticket(**params):
    show_session = sample_show_session()
    defaults = {
        "row": 5,
        "seat": 10,
        "show_session": show_session
    }
    defaults.update(params)

    return Ticket.objects.create(**defaults)


class UnauthenticatedApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reservation = sample_reservation()

    def test_auth_required_for_planetarium_dome(self):
        res = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_show_session(self):
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_reservation(self):
        res = self.client.get(reservation_detail_url(self.reservation.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="aboba@mail.com",
            password='adminpass123',
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        self.dome = sample_dome()
        self.session = sample_show_session()
        self.theme = sample_show_theme()
        payload_astronomy_show = {
            "title": "Star come back",
            "description": "Very interesting show for kids",
        }
        self.astronomy_show_for_update = sample_astronomy_show(
            **payload_astronomy_show)

    def test_get_domes_admin(self):
        res = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_domes_admin(self):
        url = dome_detail_url(1)
        payload = {
            "name": "Updated Dome",
            "rows": 15,
            "seats_in_row": 25
        }
        res = self.client.put(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_domes_not_allowed(self):
        url = dome_detail_url(1)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_domes_not_allowed(self):
        url = dome_detail_url(1)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_show_session_admin(self):
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_show_session_admin(self):
        url = session_detail_url(self.session.id)
        payload = {
            "astronomy_show": self.astronomy_show_for_update.id,
            "planetarium_dome": self.dome.id,
            "show_time": timezone.now().isoformat()
        }
        res = self.client.put(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
