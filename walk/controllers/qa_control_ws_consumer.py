import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from user_mgmt.models import AnonymousParticipant
from host.models import AnswerChoice
from walk.models import Response as AnswerResponse


class QAControlConsumer(AsyncWebsocketConsumer):

    # Handling new user connections
    async def connect(self):
        self.room_name = "qa_session_" + str(self.scope['url_route']['kwargs']['eventid'])

        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        # Accept the websocket connection
        await self.accept()

        # Updating the active user count
        count = getattr(self.channel_layer, self.room_name, 0)
        if not count:
            setattr(self.channel_layer, self.room_name, 1)
        else:
            setattr(self.channel_layer, self.room_name, count + 1)

        # Telling everyone about the active user count change
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'active_user_count'
            }
        )

    # Handling user disconnections
    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

        # Updating the active users count
        count = getattr(self.channel_layer, self.room_name, 0)
        setattr(self.channel_layer, self.room_name, count - 1)
        if count == 1:
            delattr(self.channel_layer, self.room_name)

        # Telling everyone about the active user count change
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'active_user_count'
            }
        )

    # Handling the message receiving
    async def receive(self, text_data=None, bytes_data=None):
        in_data = json.loads(text_data)

        if in_data['type'] == 'question_move':
            # Telling all the participants to switch to the next question on the list
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'question_move'
                }
            )

            # Resetting the answer count
            ac_name = self.room_name + "_answer_count"
            answer_count = getattr(self.channel_layer, ac_name, 0)
            if not answer_count:
                setattr(self.channel_layer, ac_name, 0)
            else:
                setattr(self.channel_layer, ac_name, 0)

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'answered_users_count'
                }
            )

        elif in_data['type'] == 'answer_choice':

            # Storing the answer choice
            data = in_data['data']
            participant_code = data['participant_code']
            answer_choice_id = data['answer_choice_id']
            await self.record_answer_choice(participant_code, answer_choice_id)

            # Updating and Broadcasting the answer count
            ac_name = self.room_name + "_answer_count"
            answer_count = getattr(self.channel_layer, ac_name, 0)
            if not answer_count:
                setattr(self.channel_layer, ac_name, 1)
            else:
                setattr(self.channel_layer, ac_name, answer_count + 1)

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'answered_users_count',
                    'increment_answer_id': answer_choice_id,
                },
            )

    # Recording the participant's answer choice in the db
    @database_sync_to_async
    def record_answer_choice(self, participant_code, answer_choice_id):
        participant = AnonymousParticipant.objects.get(unique_code=participant_code)
        answer = AnswerChoice.objects.get(id=answer_choice_id)
        AnswerResponse.objects.create(
            participant=participant,
            answer=answer
        )

    # Broadcasting the question move
    async def question_move(self, event):
        await self.send(
            text_data=json.dumps({
                'meant_for': 'participants',
                'type': 'question_move',
            })
        )

    # Broadcasting the count of the active users in the room
    async def active_user_count(self, event):
        n_active_users = getattr(self.channel_layer, self.room_name, 0)

        await self.send(
            text_data=json.dumps({
                'meant_for': 'all',
                'type': 'active_user_count',
                'data': {
                    'n_active_users': n_active_users,
                }
            })
        )

    # Broadcasting the count of the number of users who have answered the current question
    async def answered_users_count(self, event):
        ac_name = self.room_name + "_answer_count"
        answer_count = getattr(self.channel_layer, ac_name, 0)
        increment_answer_id = event['increment_answer_id']

        await self.send(
            text_data=json.dumps({
                'meant_for': 'all',
                'type': 'answer_count',
                'data': {
                    'n_users_answered': answer_count,
                    'increment_answer_id': increment_answer_id
                }
            })
        )
