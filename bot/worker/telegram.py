import logging

from aiotg import Bot, BotApiError, Chat

from bot.worker.base import BaseWorker


class TelegramWorker(BaseWorker):
    bot = Bot

    def __init__(self, app):
        self.app = app
        self.config = app.config

        kwargs = {
            'api_token': app.config['token'],
        }

        proxy = app.config.get('proxy', {}).get('proxy_url', '')
        if proxy:
            kwargs['proxy'] = app.config['proxy']['proxy_url']

        self.bot = Bot(**kwargs)

        self.channel = self.bot.channel(self.config['channel'])
        self.bot.add_command(r'\/?(start)', self.__start)
        self.bot.add_command(r'\/?(help)', self.__start)
        self.bot.add_command(r'.*', self.message)

    async def message(self, chat: Chat, match):
        await self.app.minecraft_worker.send_message(
            chat.message.get('from', {}).get('username', 'user'),
            chat.message.get('text', '')
        )

    async def __start(self, chat: Chat, match):
        text = 'welcome'
        return chat.send_text(text, )

    async def send_notification(self, message):
        try:
            await self.channel.send_text(message)
        except BotApiError:
            logging.error('Cant send to chat')
        pass

    def run(self):
        self.bot.loop()

    def stop(self):
        self.bot.stop()
