from aiohttp import helpers, web
from aiohttp.log import access_logger
from aiohttp.web_runner import AppRunner

from bot.worker.base import BaseWorker


class WebWorker(BaseWorker):

    def __init__(self, app):
        self.bot = app.telegram_worker
        self.web_server = web.Application(loop=app.loop)

        routes = []

        self.web_server.add_routes(routes)
        self.web_server.t = app
        self.app = app

    async def run(self):
        await web.run_app(self.web_server)

        handle_signals = True
        access_log_class = helpers.AccessLogger,
        access_log_format = helpers.AccessLogger.LOG_FORMAT,
        access_log = access_logger

        runner = AppRunner(self.web_server, handle_signals=handle_signals,
                           access_log_class=access_log_class,
                           access_log_format=access_log_format,
                           access_log=access_log)

        await runner.setup()

    def stop(self):
        pass
