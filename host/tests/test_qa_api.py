from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CreateQuestionsTestCase(TestCase):
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

    def test_successful_create_questions(self):
        user_data = {
            "event_id": self.eventId,
            "title": "The question's title goes here",
            "choices": [
                {
                    "description": "Pizza",
                    "value": 1
                },
                {
                    "description": "Ice Cream",
                    "value": 2
                },
                {
                    "description": "Salt Water",
                    "value": -1
                }
            ]
        }

        expected_out = {
            "status": "created",
            "id": 1,
        }

        resp = self.client.post('/host/qa/create/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})

        self.assertDictEqual(resp.json(), expected_out)

    def test_failure_create_questions(self):
        user_data = {
            "event_id": self.eventId,
            "title": "The question's title goes here",
            "choices": [
                {
                    "description": "Pizza",
                    "value": 1
                },
                {
                    "description": "Ice Cream",
                    "value": 2
                },
                {
                    "description": "Salt Water",
                    "value": -1
                }
            ]
        }

        expected_out = {
            "detail": "Authentication credentials were not provided."
        }

        resp = self.client.post('/host/events/create/', data=user_data)

        self.assertEqual(resp.data, expected_out)


class ViewQuestionsTestCase(TestCase):
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
        user_data = {
            "event_id": self.eventId,
            "title": "The question's title goes here",
            "choices": [
                {
                    "description": "Pizza",
                    "value": 1
                },
                {
                    "description": "Ice Cream",
                    "value": 2
                },
                {
                    "description": "Salt Water",
                    "value": -1
                }
            ]
        }

        resp = self.client.post('/host/qa/create/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})

    def test_successful_get_questions(self):
        resp = self.client.get('/host/qa/eventwise_qas/?event_id='+str(self.eventId), **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        assert response["id"] == self.eventId
        assert response["questions"][0]["description"] == "The question's title goes here"

    def test_failure_get_questions(self):

        expected_out = {
            "detail": "Authentication credentials were not provided."
        }

        resp = self.client.post('/host/qa/eventwise_qas/')

        self.assertEqual(resp.data, expected_out)
