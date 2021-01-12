import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core import models as CoreModels
from service import models as ServiceModels

from channels.db import database_sync_to_async


class LocationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'group_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        user = await database_sync_to_async(self.get_name)()

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'connected - ' + str(user)
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        GUID = message['GUID']
        location = message['location']
        await database_sync_to_async(self.update_location)(GUID, location)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': str(message)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    def update_location(self, GUID, data):
        location, created = ServiceModels.Location.objects.get_or_create()
        if created:
            location.user = CoreModels.CoreUser.objects.get(GUID=GUID)
        else:
            location.latitude = data['latitude']
            location.longitude = data['longitude']
            location.save()
        return True

    def get_name(self):
        return CoreModels.CoreUser.objects.all().first().GUID