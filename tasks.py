import asyncio
import logging

from invoke import task

logging.basicConfig(level=logging.INFO)


@task(default=True)
def run(ctx):
    """
    Run the app
    """
    from bot.app import App
    app = App(ctx.config)
    app.run()
