from youtubesearchpython.__future__ import ChannelsSearch, Video
import asyncio
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import Throttled
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.i18m_language import get_user_locale
from create_bot import _
from keyboards.markups import get_youtube_add_method_kb
from functions import youtube_url
from data_base.sqlite_db import Youtube
from states.youtube_states import AddChannel
import aioschedule


async def get_notifications_kb(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_locale(user_id)
    await message.answer(_('Настройки', locale=user_lang))







def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(get_notifications_kb, text_contains=['Уведомления'])