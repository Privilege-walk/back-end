from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CreateEventTestCase(TestCase):
    def setUp(self) -> None:
        usr = User.objects.create_user(username = "12thMan", email = "twelve@testtamu.edu", password = "SomePassword123")
        usr.first_name = "12th"
        usr.last_name = "Man"
        usr.save()
        self.user_auth_token, _ = Token.objects.get_or_create(user=usr)

    def test_successful_create_event(self):
        user_data = {
            "name": "A new year event"
        }
        headers = {
            'HTTP_X_HTTP_METHOD_OVERRIDE': 'PUT',
            "Authorization":"Token "+ self.user_auth_token.key
        }

        expected_out = {
            "status": "created",
            "id": 1,
        }

        resp = self.client.post('/host/events/create/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})

        self.assertDictEqual(resp.json(), expected_out)

    def test_failure_create_event(self):
        user_data = {
            "name": "A new year event"
        }

        expected_out = {
            "detail": "Authentication credentials were not provided."
        }

        resp = self.client.post('/host/events/create/', data=user_data)

        self.assertEqual(resp.data, expected_out)


class ViewEventsTestCase(TestCase):
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


    def test_successful_get_event(self):

        expected_out = {
            "events": [
        {
            "id": 1,
            "name": "A new year event",
            "status": "created"
        }]
        }

        resp = self.client.get('/host/events/all/', **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})

        self.assertDictEqual(resp.json(), expected_out)

    def test_failure_get_event(self):

        expected_out = {
            "detail": "Authentication credentials were not provided."
        }

        resp = self.client.post('/host/events/all/')

        self.assertEqual(resp.data, expected_out)
