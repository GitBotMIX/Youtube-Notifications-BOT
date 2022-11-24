from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from data_base.sqlite_db import User


class SetLanguage(BaseMiddleware):
    def __init__(self):
        super(SetLanguage, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        user_lang = await User.Language.get_language(user_id)
        data["user_lang"] = user_lang
        # raise CancelHandler()
