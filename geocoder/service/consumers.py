import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core import models as CoreModels
from service import models as ServiceModels

from channels.db import database_sync_to_async
from math import asin, cos, radians, sin, sqrt
from core import serializers

import logging
logger = logging.getLogger(__name__)

import requests


class LocationConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'group_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'connected'
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
        is_client = bool(message['is_client'])
        # logger.error(is_client)
        await database_sync_to_async(self.update_location)(GUID, is_client, location)

    def update_location(self, GUID, is_client, data):

        location, created = ServiceModels.Location.objects.get_or_create(user__GUID=GUID)
        if created:
            location.user = CoreModels.CoreUser.objects.get(GUID=GUID)
            location.is_client = bool(is_client)

        location.latitude = data['latitude']
        location.longitude = data['longitude']
        location.save()

        return True


class RideRequestConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'group_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'connected'
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
        is_client = bool(message['is_client'])

        # logger.error(is_client)
        await database_sync_to_async(self.update_location)(GUID, is_client, location)

        ride = await database_sync_to_async(self.check_mention)(GUID)
        if ride:
            await self.send(text_data=json.dumps({
                'message': serializers.RideSerializer(ride).data
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': serializers.RideSerializer(ride).data
            }))

    def update_location(self, GUID, is_client, data):

        location, created = ServiceModels.Location.objects.get_or_create(user__GUID=GUID)
        if created:
            location.user = CoreModels.CoreUser.objects.get(GUID=GUID)
            location.is_client = bool(is_client)

        location.latitude = data['latitude']
        location.longitude = data['longitude']
        location.save()

        return True

    def check_mention(self, GUID):

        mention, created = ServiceModels.Mention.objects.get_or_create(user__GUID=GUID)
        if created:
            mention.user = CoreModels.CoreUser.objects.get(GUID=GUID)
            mention.active = False

        if mention.active:
            ride = mention.ride

            return ride

        return False
