from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import _
from i18m_language import get_user_locale


async def get_youtube_add_method_kb(user_id):
    user_lang = await get_user_locale(user_id)
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
