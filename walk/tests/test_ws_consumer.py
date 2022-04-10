import json

from django.test import TestCase
from channels.testing import WebsocketCommunicator

from privilege_walk_be.asgi import application\


class QAConsumerTest(TestCase):
    def setUp(self) -> None:
        pass

    async def test_connectivity(self):

        self.communicator = WebsocketCommunicator(application, "/ws/walk/qa_control/12/")
        connected, subprotocol = await self.communicator.connect()
        self.assertEqual(connected, True)

        # Testing the initial active user count change
        expected = {
                'meant_for': 'all',
                'type': 'active_user_count',
                'data': {
                    'n_active_users': 1,
                }
            }

        raw_message = await self.communicator.receive_from()
        message = json.loads(raw_message)

        self.assertEqual(message, expected)