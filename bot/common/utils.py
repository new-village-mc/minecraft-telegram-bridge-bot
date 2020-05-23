import logging
import pathlib
import re
from datetime import datetime

import aiohttp

re_class_name = re.compile(r'([A-Z]*[a-z]*)')


def parse_time(s):
    """ Parse 12-hours format """
    return datetime.strptime(s, '%I:%M %p')


def allowed_users(function):
    async def wrapper_about_function(self, chat, match):
        if chat.sender['username'] in self.config.allowed_users:

            await function(self, chat, match)

        else:
            chat.bot.send_message(chat_id=chat.id,
                                  text='You are not allowed to use this bot.')

    return wrapper_about_function


def get_dict_templates(path_file):
    path = pathlib.Path(__file__).parent.parent
    work_dir = path / path_file
    dict_templates = {}
    for file in work_dir.iterdir():
        dict_templates[file.name] = file.read_text(encoding='utf-8')
    return dict_templates


async def get(path, params, headers):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(path, params=params) as r:
            result = await r.json()
            logging.info(f'/GET: path {path} status {result}')
            logging.info(headers)
            return result


async def post(path, headers, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(path, data=data) as r:
            result = r.json()
            logging.info(f'/POST: path {path} status {result}')
            logging.info(headers)


async def put(path, headers, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.put(path, data=data) as r:
            result = await r.json()
            logging.info(f'/PUT: path {path} status {result}')
            logging.info(headers)


class classproperty(object):  # noqa
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def convert_class_name(name):
    """
    >>> convert_class_name('ClassName')
    'class_name'
    >>> convert_class_name('ABClassName')
    'abclass_name'
    """
    li = re_class_name.findall(name)
    return '_'.join(i.lower() for i in li if i)
