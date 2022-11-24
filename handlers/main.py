from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.throttling import large_numbers_requests
from middlewares.i18m_language import get_user_locale
from create_bot import _
from keyboards.youtube_main_kb import get_youtube_main_kb


@dp.throttled(large_numbers_requests, rate=5)
async def start_message(message: types.Message):
    user_id = message.from_user.id
    await message.answer('Добро пожаловать', reply_markup=await get_youtube_main_kb(user_id))


@dp.throttled(large_numbers_requests, rate=1)
async def get_main_kb(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_locale(user_id)
    await message.answer(_('Главное меню', locale=user_lang), reply_markup=await get_youtube_main_kb(user_id))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start'])
    dp.register_message_handler(get_main_kb, commands=['назад', 'back', 'home'], state='*')

