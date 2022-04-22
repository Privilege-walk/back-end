import json

from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator

from privilege_walk_be.asgi import application

from user_mgmt.models import AnonymousParticipant
from host.models import Event, Question, AnswerChoice
from django.contrib.auth.models import User

class QAConsumerTest(TransactionTestCase):
    def setUp(self) -> None:
        host_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='howdy1234'
        )

        eve = Event.objects.create(
            host=host_user,
            name='Birthday',
            status='Created',
        )

        ques = Question.objects.create(
            event=eve,
            description='Do you like cake?'
        )

        ans = AnswerChoice.objects.create(
            question=ques,
            description='yes',
            value=1
        )

        self.answer_id = ans.id

        anno_part = AnonymousParticipant.objects.create(
            event=eve
        )

        anno_part.save()
        self.participant_code = anno_part.unique_code

    async def test_channel(self):

        ### Testing Connectivity

        communicator = WebsocketCommunicator(application, "/ws/walk/qa_control/12/")
        connected, subprotocol = await communicator.connect()
        self.assertEqual(connected, True)

        # Testing the initial active user count change
        expected = {
            'meant_for': 'all',
            'type': 'active_user_count',
            'data': {
                'n_active_users': 1,
            }
        }

        raw_message = await communicator.receive_from()
        message = json.loads(raw_message)

        self.assertEqual(message, expected)


        ### Testing the question move orders

        # Host side
        await communicator.send_to(json.dumps({
            "type": "question_move"
        }))

        # Participant side
        expected = {
            "meant_for": "participants",
            "type": "question_move",
        }
        raw_message = await communicator.receive_from()
        message = json.loads(raw_message)
        self.assertEqual(message, expected)


        ### Testing the answer choice messages

        # Participant Side
        # await communicator.send_to(
        #     json.dumps({
        #         "type": "answer_choice",
        #         "data": {
        #             "participant_code": self.participant_code,
        #             "answer_choice_id": self.answer_id
        #         }
        #     })
        # )
        #
        # # Everyone gets a responded count
        # expected = {
        #     "meant_for": "all",
        #     "type": "answer_count",
        #     "data": {
        #         "n_users_answered": 1,
        #     }
        # }
        #
        # print("Sending to the comm")
        # raw_message = await communicator.receive_from()
        # message = json.loads(raw_message)
        # print("Comm done")
        #
        # print("WS Message")
        # print(message)
        #
        # self.assertEqual(message, expected)
        #
        # await communicator.disconnect()
