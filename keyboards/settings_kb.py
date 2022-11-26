from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from middlewares.i18m_language import get_user_locale


async def get_buttons_en():
    b1 = KeyboardButton('🇷🇺/🇬🇧Language')
    b2 = KeyboardButton('↩Back')
    return b1, b2


async def get_buttons_ru():
    b1 = KeyboardButton('🇷🇺Язык | Language🇬🇧')
    b2 = KeyboardButton('↩Назад')
    return b1, b2


async def get_settings_main_kb(user_id=None, user_lang=None):
    if not user_lang:
        user_lang = await get_user_locale(user_id)
    if user_lang == 'en':
        b1, b2 = await get_buttons_en()
    else:
        b1, b2 = await get_buttons_ru()

    kb_settings = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_settings.add(b1).add(b2)
