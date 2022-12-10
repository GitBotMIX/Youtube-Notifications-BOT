from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import _
from middlewares.i18m_language import get_user_locale


async def get_language_choose_kb(user_id, user_lang=None):
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    b1 = InlineKeyboardButton(text=_('🇷🇺Русский', locale=user_lang),
                              callback_data='set_user_language ru')
    b2 = InlineKeyboardButton(text=_('🇬🇧English', locale=user_lang),
                              callback_data='set_user_language en')
    language_choose_kb = InlineKeyboardMarkup(resize_keyboard=False)
    return language_choose_kb.row(b1, b2)


async def get_youtube_add_method_kb(user_id, user_lang=None):
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    b1 = InlineKeyboardButton(text=_('По названию канала', locale=user_lang),
                              callback_data='youtube_add_method channel_name')
    b2 = InlineKeyboardButton(text=_('По ссылке на канал', locale=user_lang),
                              callback_data='youtube_add_method channel_url')
    b3 = InlineKeyboardButton(text=_('По ссылке на видео', locale=user_lang),
                              callback_data='youtube_add_method channel_video_url')
    b4 = InlineKeyboardButton(text=_('Ничего не понимаю...', locale=user_lang),
                              callback_data='youtube_add_method help')
    youtube_add_method_inline_kb = InlineKeyboardMarkup(resize_keyboard=False)
    return youtube_add_method_inline_kb.add(b1).row(b2, b3).add(b4)
