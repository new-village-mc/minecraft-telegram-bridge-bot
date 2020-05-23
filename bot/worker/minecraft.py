import json
import logging

import websockets
try:
    import thread
except ImportError:
    import _thread as thread

from bot.worker.base import BaseWorker


class MinecraftWorker(BaseWorker):

    def __init__(self, app):
        self.app = app
        self.uri = app.config.get('minecraft', {}).get('uri', 'ws://localhost:8090')
        self.running = True
        self.ws = None

    async def process_message(self, message):
        msg = {}
        try:
            msg = json.loads(message)
        except:
            logging.info('got welcome msg')
            return

        if msg.get('type') == 'message':
            message_text = msg.get('data', {}).get('text')
            message_author = msg.get('data', {}).get('author')
            await self.app.telegram_worker.send_notification(f'{message_author}: {message_text}')
        elif msg.get('type') == 'webmap':
            message_text = msg.get('data', {}).get('text')
            await self.app.telegram_worker.send_notification(message_text)

    async def send_message(self, name, text):
        msg = {
            'type': 'message',
            'data': {
                'text': text,
                'author': name,
            }
        }

        json_msg = json.dumps(msg)
        await self.ws.send(json_msg)

    async def run(self):
        async with websockets.connect(self.uri) as websocket:
            self.ws = websocket
            while self.running:
                message = await websocket.recv()
                await self.process_message(message)

    async def stop(self):
        pass
