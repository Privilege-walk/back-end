import json

from django.test import TestCase
from channels.testing import WebsocketCommunicator

from privilege_walk_be.asgi import application

class QAConsumerTest(TestCase):
    def setUp(self) -> None:
        pass

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
