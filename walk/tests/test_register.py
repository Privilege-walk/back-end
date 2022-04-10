from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ParticipantRegistrationTestCase(TestCase):
    def setUp(self) -> None:
        usr = User.objects.create_user(username = "12thMan", email = "twelve@testtamu.edu", password = "SomePassword123")
        usr.first_name = "12th"
        usr.last_name = "Man"
        usr.save()
        self.user_auth_token, _ = Token.objects.get_or_create(user=usr)

        user_data = {
            "name": "A new year event"
        }
        resp = self.client.post('/host/events/create/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        self.eventId = response["id"]

    def test_successful_registration(self):
        user_data = {
            "event_id": self.eventId
        }

        resp = self.client.post('/walk/register_participant/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        assert response['status'] == "registered"

    def test_failure_registration_no_eventid(self):
        user_data = {
            "event_id": ''
        }

        resp = self.client.post('/walk/register_participant/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        assert response['message'] == "Event not found, try a different event ID"

    def test_failure_registration_wrong_eventid(self):
        user_data = {
            "event_id": '12345'
        }

        resp = self.client.post('/walk/register_participant/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        assert response['message'] == "Event not found, try a different event ID"



