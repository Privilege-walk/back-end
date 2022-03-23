from django.test import TestCase

from django.contrib.auth.models import User
from user_mgmt.models import AnonymousParticipant
from host.models import Event


class AnonymousParticipantTestCase(TestCase):
    def setUp(self) -> None:
        sample_user = User.objects.create_user(
            username="sampleuser",
            password="Howdy1234",
            email="sampleuser@email.com",
        )

        sample_event = Event.objects.create(
            host=sample_user,
            name="Test Event",
            status="Created"
        )
        AnonymousParticipant.objects.create(
            event=sample_event
        )
        AnonymousParticipant.objects.create(
            event=sample_event
        )

        self.test_event = sample_event

    def test_unique_user_code_auto_generation(self):
        part_1, part_2 = AnonymousParticipant.objects.all()

        self.assertNotEqual(part_1.unique_code, "")
        self.assertNotEqual(part_2.unique_code, "")

    def test_unique_user_code_manual_generation(self):
        some_participant = AnonymousParticipant.objects.create(
            event=self.test_event
        )

        regenerated_participant_code = some_participant.generate_unique_code()
        self.assertNotEqual(regenerated_participant_code, some_participant.unique_code)

    def test_unique_user_code_format(self):
        part_1, part_2 = AnonymousParticipant.objects.all()

        self.assertEqual(len(part_1.unique_code), 4)
        self.assertEqual(len(part_2.unique_code), 4)

    def test_unique_user_code_uniqueness(self):
        part_1, part_2 = AnonymousParticipant.objects.all()

        self.assertNotEqual(part_2.unique_code, part_1.unique_code)