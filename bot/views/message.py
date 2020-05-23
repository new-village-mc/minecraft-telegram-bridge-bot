from aiohttp import web
from aiohttp.web_exceptions import HTTPForbidden


async def message_post(request):
    bot = request.app.t.telegram_worker

    config = request.app.t.config
    token = config.get('api', {}).get('token')

    if request.headers.get('API-KEY') != token:
        raise HTTPForbidden()

    data = await request.json()

    await bot.send_notification(data.get('message', "🚨 something happened"))

    return web.Response()
