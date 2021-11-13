# chat/consumers.py
import json
from channels.consumer import AsyncConsumer
import asyncio
from .tail import Tail
import logging

logger = logging.getLogger('django')


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.connected = True

        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

        while self.connected:

            await asyncio.sleep(0.5)

            t = Tail('debug.log')
            async for line in t.follow():
                data = json.dumps({'message': line})
                await self.send({
                    'type': 'websocket.send',
                    'text': data
                })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        self.connected = False
