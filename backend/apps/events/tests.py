from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Event


class EventModelTests(TestCase):
    def test_event_can_be_created(self):
        event = Event.objects.create(
            title="Community Meetup",
            description="A casual get-together for the local community.",
            location="Community Hall",
            date="2026-10-01 18:00:00+00:00",
            capacity=50,
        )
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.title, "Community Meetup")

    def test_required_fields_cannot_be_blank(self):
        event = Event(
            title="",
            description="",
            location="",
            date=None,
            capacity=None,
        )
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_capacity_accepts_valid_positive_value(self):
        event = Event.objects.create(
            title="Workshop",
            description="Hands-on workshop session.",
            location="Room 101",
            date="2026-11-05 09:00:00+00:00",
            capacity=20,
        )
        self.assertEqual(event.capacity, 20)

    def test_event_is_stored_correctly(self):
        Event.objects.create(
            title="Conference",
            description="Annual tech conference.",
            location="Main Auditorium",
            date="2026-12-15 10:00:00+00:00",
            capacity=200,
        )
        saved_event = Event.objects.get(title="Conference")
        self.assertEqual(saved_event.description, "Annual tech conference.")
        self.assertEqual(saved_event.location, "Main Auditorium")
        self.assertEqual(saved_event.capacity, 200)


class EventAPITests(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Tech Talk",
            description="A talk about technology.",
            location="Auditorium",
            date="2026-10-01 18:00:00+00:00",
            capacity=100,
        )

    def test_list_events_returns_all_events(self):
        url = reverse("event-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Tech Talk")

    def test_retrieve_event_returns_correct_event(self):
        url = reverse("event-detail", kwargs={"pk": self.event.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.event.pk)
        self.assertEqual(response.data["title"], "Tech Talk")
        self.assertEqual(response.data["location"], "Auditorium")
        self.assertEqual(response.data["capacity"], 100)

    def test_retrieve_event_with_invalid_id_returns_404(self):
        invalid_pk = self.event.pk + 9999
        url = reverse("event-detail", kwargs={"pk": invalid_pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
