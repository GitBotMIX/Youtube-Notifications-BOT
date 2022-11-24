from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from data_base.sqlite_db import User


class RegisterCheck(BaseMiddleware):
    def __init__(self):
        super(RegisterCheck, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        if not await User.get_user(user_id):
            await User.add('default', 'ru', str(user_id))
            print('Add user')
        # raise CancelHandler()
