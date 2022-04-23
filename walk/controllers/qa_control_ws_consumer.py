import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Sum

from user_mgmt.models import AnonymousParticipant
from host.models import AnswerChoice, Event, Question
from walk.models import Response as AnswerResponse, Response


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
        ac_name = self.room_name + "_active_user_count"
        count = getattr(self.channel_layer, ac_name, 0)
        if not count:
            setattr(self.channel_layer, ac_name, 1)
        else:
            setattr(self.channel_layer, ac_name, count + 1)

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
        ac_name = self.room_name + "_active_user_count"
        count = getattr(self.channel_layer, ac_name, 0)
        setattr(self.channel_layer, ac_name, count - 1)
        if count == 1:
            delattr(self.channel_layer, ac_name)

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

            # Updating and Broadcasting the answer count and the answer ID increment
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


            # Broadcasting the live user line position counts for the host graph
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'user_positions',
                },
            )


    # Broadcasting the line position counts for the event
    async def user_positions(self, event):
        event_id = int(self.room_name.split("_")[-1])
        position_stats = await self.get_bars_statistics(event_id)

        await self.send(
            text_data=json.dumps({
                'meant_for': 'host',
                'type': 'line_counts',
                'data': {
                    'position_stats': position_stats,
                }
            })
        )


    # Getting the line statistics
    async def get_bars_statistics(self, event_id):
        event_questions = await self.get_event_questions(event_id)
        choices = await self.get_answer_choices(event_questions)
        positions = await self.get_positions(choices)

        position_counts = {}

        for position in positions:
            pos = position['position']
            if pos in position_counts:
                position_counts[pos] += 1
            else:
                position_counts[pos] = 1

        return position_counts

    @database_sync_to_async
    def get_event_questions(self, event_id):
        event_questions = Question.objects.filter(event__id=event_id)
        return list(event_questions)

    @database_sync_to_async
    def get_answer_choices(self, event_questions):
        choices = AnswerChoice.objects.filter(question__in=event_questions)
        return list(choices)

    @database_sync_to_async
    def get_positions(self, choices):
        positions = Response.objects.filter(answer__in=choices).values('participant').annotate(
            position=Sum('answer__value')).order_by('position')
        return list(positions)

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
        ac_name = self.room_name + "_active_user_count"
        n_active_users = getattr(self.channel_layer, ac_name, 0)

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
        increment_answer_id = 0

        if 'increment_answer_id' in event:
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
