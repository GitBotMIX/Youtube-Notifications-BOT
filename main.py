from aiogram.utils import executor
from create_bot import dp, bot
from data_base import sqlite_db
from middlewares import register_check, set_language
import asyncio


async def start(*args):
    print('Youtube Notifications bot start')
    sqlite_db.sql_start()


from handlers import youtube, main

main.register_handlers_client(dp)
youtube.register_handlers_client(dp)

if __name__ == '__main__':
    dp.middleware.setup(register_check.RegisterCheck())
    dp.middleware.setup(set_language.SetLanguage())
    executor.start_polling(dp, skip_updates=True, on_startup=start)
