from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from middlewares.i18m_language import get_user_locale


async def get_buttons_en():
    b1 = KeyboardButton('✔Add channel')
    b2 = KeyboardButton('✖Delete channel')
    b3 = KeyboardButton('⚙Settings')
    return b1, b2, b3


async def get_buttons_ru():
    b1 = KeyboardButton('✔Добавить канал')
    b2 = KeyboardButton('✖Удалить канал')
    b3 = KeyboardButton('⚙Настройки')
    return b1, b2, b3


async def get_youtube_main_kb(user_id, user_lang=None):
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    user_lang = await get_user_locale(user_id)
    if user_lang == 'en':
        b1, b2, b3 = await get_buttons_en()
    else:
        b1, b2, b3 = await get_buttons_ru()

    kb_youtube_main = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_youtube_main.row(b1, b2).add(b3)
