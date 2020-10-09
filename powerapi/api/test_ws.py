import pytest

from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from django.conf import settings

from .notifier import Notifier


@pytest.mark.asyncio
async def test_notification():
    communicator = WebsocketCommunicator(application=Notifier, path='/ws/notification/')
    connected, _ = await communicator.connect()
    assert connected

    message = {'active': 0.1, 'reactive': 0.05}

    channel_layer = get_channel_layer()
    await channel_layer.group_send(settings.NOTIFY_GROUP, {'type': 'notify', 'message': message})
    socket_response = await communicator.receive_json_from(timeout=5)

    assert message == socket_response

    await communicator.disconnect()
