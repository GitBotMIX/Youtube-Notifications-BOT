from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from middlewares.i18m_language import get_user_locale


async def get_buttons_en():
    b1 = KeyboardButton('/Add channel')
    b2 = KeyboardButton('/Delete channel')
    return b1, b2


async def get_buttons_ru():
    b1 = KeyboardButton('/Добавить канал')
    b2 = KeyboardButton('/Удалить канал')
    return b1, b2


async def get_youtube_main_kb(user_id):
    user_lang = await get_user_locale(user_id)
    if user_lang == 'en':
        b1, b2 = await get_buttons_en()
    else:
        b1, b2 = await get_buttons_ru()

    kb_youtube_main = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_youtube_main.add(b1).add(b2)
