from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from user_mgmt.models import AnonymousParticipant
from host.models import AnswerChoice, Event, Question
from walk.models import Response as AnswerResponse, Response

class GetQAStatsTestCase(TestCase):
    def setUp(self) -> None:
        usr = User.objects.create_user(username = "12thMan", email = "twelve@testtamu.edu", password = "SomePassword123")
        usr.first_name = "12th"
        usr.last_name = "Man"
        usr.save()
        self.user_auth_token, _ = Token.objects.get_or_create(user=usr)

        user_data = {
            "name": "A new year event",
            "x_label_min": "Some text to be displayed on the graph",
            "x_label_max": "Something else you want to be displayed on the graph",
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
        response = resp.json()
        question_id = response["id"]
        user_data = {
            "event_id": self.eventId
        }

        resp = self.client.post('/walk/register_participant/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        participant_code = response["participant_code"]
        
        question = Question.objects.get(id=question_id)
        participant = AnonymousParticipant.objects.get(unique_code=participant_code)
        answer = AnswerChoice.objects.filter(question = question)

        AnswerResponse.objects.create(
            participant=participant,
            answer=answer[0]
        )

        resp = self.client.post('/walk/register_participant/', content_type='application/json', data=user_data, **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        participant_code = response["participant_code"]
        participant = AnonymousParticipant.objects.get(unique_code=participant_code)
        AnswerResponse.objects.create(
            participant=participant,
            answer=answer[0]
        )

    def test_successful_get_qa_stats(self):
        resp = self.client.get('/host/qa_stats/?event_id='+str(self.eventId) , **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        response = resp.json()
        assert response[0]["question_id"] == 1
        assert response[0]["question"] == "The question's title goes here"
        assert response[0]["answers"][0]["count"] == 2

    def test_get_qa_stats_no_event_id(self):
        resp = self.client.get('/host/qa_stats/' , **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        expected_out = {
            "message": "Please enter an event ID"
        }

        self.assertEqual(resp.data, expected_out)

    def test_get_qa_stats_wrong_event_id(self):
        resp = self.client.get('/host/qa_stats/?event_id='+str(999) , **{'HTTP_AUTHORIZATION':'Token '+ self.user_auth_token.key})
        expected_out = {
            "message": "The event ID that you've entered is not in the records"
        }

        self.assertEqual(resp.data, expected_out)