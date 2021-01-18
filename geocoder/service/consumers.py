import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core import models as CoreModels
from service import models as ServiceModels

from channels.db import database_sync_to_async
from math import asin, cos, radians, sin, sqrt
import haversine


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


class RideRequestConsumer(AsyncWebsocketConsumer):

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
        await database_sync_to_async(self.SearchClosest)(GUID, location)

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

    def search_closest(self, GUID, data):
        location, created = ServiceModels.Location.objects.get_or_create()
        if created:
            location.user = CoreModels.CoreUser.objects.get(GUID=GUID)
        else:
            location.latitude = data['latitude']
            location.longitude = data['longitude']
            location.save()
        return True

    def dist_between_two_lat_lon(self, *args):
        lat1, lat2, long1, long2 = map(radians, args)

        dist_lats = abs(lat2 - lat1)
        dist_longs = abs(long2 - long1)
        a = sin(dist_lats/2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs/2)**2
        c = asin(sqrt(a)) * 2
        radius_earth = 6378
        # the "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
        return c * radius_earth

    def find_closest_lat_lon(self, data, v):
        try:
            return min(
                data,
                key=lambda p: dist_between_two_lat_lon(v['lat'], v['lon'], p['lat'], p['lon']))
        except TypeError:
            print('Not a list or not a number.')

    def get_name(self):
        return CoreModels.CoreUser.objects.all().first().GUID
