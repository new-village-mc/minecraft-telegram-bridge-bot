import logging

from aiohttp import web
from aiohttp.web_exceptions import HTTPForbidden
from jinja2 import Template

work_dir = './bot/templates/prometheus_alert/'
template = Template(open(work_dir + 'alert', encoding="utf-8").read())


async def prometheus_post(request):
    data = await request.json()
    bot = request.app.t.telegram_worker

    config = request.app.t.config
    token = config.get('prometheus', {}).get('token')

    if request.headers.get('Authorization') is f'Bearer {token}':
        logging.error(f"Forboden for token '{request.headers.get('Authorization')}'")
        raise HTTPForbidden()

    message = template.render(alerts=data.get('alerts'))
    await bot.send_notification(message)
    return web.Response()
