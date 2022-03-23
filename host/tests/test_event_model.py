from django.test import TestCase

from django.contrib.auth.models import User
from host.models import Event


class TestEvents(TestCase):
    def setUp(self) -> None:
        self.event_host_user = User.objects.create_user(
            username="sampleuser",
            password="somepassword",
            email="sampleuser@email.com"
        )

    def test_event_creation(self):
        Event.objects.create(
            host=self.event_host_user,
            name="Rodeo",
            status="created"
        )

        created_event = Event.objects.get(id=1)
        self.assertEqual(created_event.name, "Rodeo")
