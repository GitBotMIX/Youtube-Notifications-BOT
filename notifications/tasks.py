import aioschedule
import asyncio
from functions import youtube_url
from data_base.sqlite_db import Youtube, User
from create_bot import bot
import datetime
import time
from notifications import youtube_listener


class Scheduler:
    async def make_task(self):
        aioschedule.every(30).seconds.do(youtube_listener.listen)
        #aioschedule.every().day.at('1:00').do(reset_requests_amount)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)