import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Sum

from user_mgmt.models import AnonymousParticipant
from host.models import AnswerChoice, Event, Question
from walk.models import Response as AnswerResponse, Response


class QAControlConsumer(AsyncWebsocketConsumer):

    def get_question_index_name(self):
        # gets the name of the channel layer attribute that stores the question index
        return self.room_name + "_question_index"

    # Handling new user connections
    async def connect(self):
        self.event_id = str(self.scope['url_route']['kwargs']['eventid'])
        self.room_name = "qa_session_" + self.event_id

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

        # Get the current question index
        question_index_name = self.get_question_index_name()
        # when question_index == -1, this means event hasn't yet started
        question_index = getattr(self.channel_layer, question_index_name, -1)
        if question_index == -1:
            setattr(self.channel_layer, question_index_name, question_index)


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
            question_index = in_data["data"]["questionIndex"]
            setattr(self.channel_layer, self.get_question_index_name(), question_index)
            
            # Telling all the participants to switch to the next question on the list
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'question_move',
                }
            )

            # if event has ended
            end_event = in_data["data"]["endEvent"]
            print(in_data)
            if end_event:
                await self.update_event_status(self.event_id, "Ended")

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
        event_users = await self.get_event_users(event_id)

        position_counts = {}

        for user in event_users:
            user_code = user.unique_code

            user_position = await self.get_user_position(user_code)

            if user_position in position_counts:
                position_counts[user_position] += 1
            else:
                position_counts[user_position] = 1

        return position_counts

    @database_sync_to_async
    def get_event_users(self, event_id):
        event_users = AnonymousParticipant.objects.filter(event__id=event_id)
        return list(event_users)

    @database_sync_to_async
    def get_user_position(self, participant_code):
        participant_responses = Response.objects.filter(participant__unique_code=participant_code)

        response_answer_values = []
        for response in participant_responses:
            response_answer_values.append(response.answer.value)

        return sum(response_answer_values)

    # Recording the participant's answer choice in the db
    @database_sync_to_async
    def record_answer_choice(self, participant_code, answer_choice_id):
        participant = AnonymousParticipant.objects.get(unique_code=participant_code)
        answer = AnswerChoice.objects.get(id=answer_choice_id)
        AnswerResponse.objects.create(
            participant=participant,
            answer=answer
        )

    @database_sync_to_async
    def update_event_status(self, event_id, event_status):
        event = Event.objects.get(id=event_id)
        event.status = event_status
        event.save()

    # Broadcasting the question move
    async def question_move(self, event):
        question_index = getattr(self.channel_layer, self.get_question_index_name(), -1)
        await self.send(
            text_data=json.dumps({
                'meant_for': 'participants',
                'type': 'question_move',
                'data': {
                        # specifies question index to move to in case a participant lost connection
                        'question_index': question_index
                    }
            })
        )

    # Broadcasting the count of the active users in the room
    async def active_user_count(self, event):
        ac_name = self.room_name + "_active_user_count"
        n_active_users = getattr(self.channel_layer, ac_name, 0)
        question_index = getattr(self.channel_layer, self.get_question_index_name(), -1)

        await self.send(
            text_data=json.dumps({
                'meant_for': 'all',
                'type': 'active_user_count',
                'data': {
                    'n_active_users': n_active_users,
                    # incase participants loose connection and are left behind, 
                    # question_index lets participants know the current question in the event
                    'question_index': question_index 
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
