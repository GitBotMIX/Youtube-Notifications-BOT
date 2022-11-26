from aiogram import types, Dispatcher
from create_bot import dp
from create_bot import _
from keyboards.settings_kb import get_settings_main_kb
from data_base.sqlite_db import User
from handlers.throttling import large_numbers_requests, throttling_alert
from aiogram.utils.exceptions import Throttled


@dp.throttled(throttling_alert, rate=3)
async def get_settings_kb(message: types.Message, user_lang):
    await message.answer(_('Настройки', locale=user_lang), reply_markup=await get_settings_main_kb(user_lang=user_lang))


@dp.throttled(throttling_alert, rate=4)
async def set_language(message: types.Message, user_lang):
    user_id = message.from_user.id
    if user_lang == 'ru':
        new_language = 'en'
    else:
        new_language = 'ru'
    lang_symbols = {'ru': '🇷🇺', 'en': '🇬🇧'}
    await User.Language.update(new_language, user_id)
    await message.answer(_('{}Язык интерфейса обновлен', locale=new_language).format(lang_symbols[new_language]),
                         reply_markup=await get_settings_main_kb(user_lang=new_language))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(get_settings_kb,
                                lambda msg: any(i in msg.text.lower() for i in ['настройки', 'settings']))
    dp.register_message_handler(set_language,
                                lambda msg: any(i in msg.text.lower() for i in ['язык', 'language']))