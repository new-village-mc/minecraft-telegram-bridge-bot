import asyncio
from concurrent.futures import ProcessPoolExecutor

from aiohttp.web import run_app

from bot.worker.minecraft import MinecraftWorker
from bot.worker.telegram import TelegramWorker
from bot.worker.web_worker import WebWorker


class App:

    def __init__(self, config):

        # Some base configuring
        self.config = config

        # Some bullshit to remove
        self.loop = asyncio.get_event_loop()
        self.executor = ProcessPoolExecutor(max_workers=4)

        # Workers
        self.telegram_worker = TelegramWorker(self)
        self.web_worker = WebWorker(self)
        self.minecraft_worker = MinecraftWorker(self)

    async def init(self, loop):
        async def background_tasks(app):
            app['telegram_worker'] = app.loop.create_task(app.t.telegram_worker.bot.loop())
            app['minecraft_worker'] = app.loop.create_task(app.t.minecraft_worker.run())
        self.web_worker.web_server.on_startup.append(background_tasks)
        return self.web_worker.web_server

    def run(self):
        app = self.loop.run_until_complete(self.init(self.loop))
        run_app(app)
