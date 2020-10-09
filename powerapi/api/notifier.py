from django.conf import settings
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class Notifier(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(settings.NOTIFY_GROUP, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(settings.NOTIFY_GROUP, self.channel_name)

    async def notify(self, event):
        message = event['message']

        await self.send_json(message)
