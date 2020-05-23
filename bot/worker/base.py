import asyncio
import datetime
import logging
from abc import ABC, abstractmethod

import pytz
from crontab import CronTab


class BaseWorker(ABC):

    _run = False

    @abstractmethod
    async def run(self):
        pass

    @abstractmethod
    async def stop(self):
        pass


class CronWorker(BaseWorker, ABC):

    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.timezone = pytz.timezone(
            app.config['time_settings']['timezone']
        )
        self._run = False
        self.schedule = CronTab(self.config['schedule'])
        self.interval = self.config['interval']

    @abstractmethod
    async def _job(self):
        pass

    async def run(self):
        self._run = True

        while self._run:
            now = datetime.datetime.now(self.timezone)
            if self.schedule.next(now) < self.interval:
                try:
                    await self._job()
                except Exception as exc:
                    logging.error(exc)

            await asyncio.sleep(self.interval)

    async def stop(self):
        self._run = False
