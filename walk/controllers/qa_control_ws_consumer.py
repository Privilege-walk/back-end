import json
from channels.generic.websocket import AsyncWebsocketConsumer


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
        pass

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
