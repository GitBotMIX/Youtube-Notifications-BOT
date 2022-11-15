from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.throttling import large_numbers_requests
from i18m_language import get_user_locale
from create_bot import _
from keyboards.youtube_main_kb import get_youtube_main_kb
from functions import youtube_url
from data_base.sqlite_db import Youtube as Youtube_db
Youtube_db = Youtube_db()

from states import youtube_states


async def add_youtube_channel(message: types.Message):
    user_id = message.from_user.id
    youtube_channel_list = await Youtube_db.channel(from)
    print(youtube_channel_list)
    if len(youtube_channel_list) >= 4:
        await message.answer('Достигнут лимит по отслеживаемым каналам, чтобы отслеживать более 4 каналов необходимо '
                             'преобрести премиум, что-бы преобрести премиум воспользуйся командой - /get_premium')
        return
    await message.answer('Введи ссылку на канал:')
    #account_status = await Youtube_db.get_all_row_in_table_where('account', 'status', 'user_id', user_id)
    #if not account_status:
    #    await Youtube_db.sql_account_add(user_id)
    #await youtube_states.AddChannel.message.set()
    #await youtube_states.AddChannel.next()

"""
async def channel_name_corrector(channel_name):
    if len(channel_name) > 30:
        channel_name = channel_name[0:30]
    return channel_name


async def add_youtube_channel_set(message: types.Message, state: FSMContext):
    message_text = await youtube_url.url_corrector(message.text)
    channel_name = await youtube_url.check(message_text)
    user_id = str(message.from_user.id)
    url_user_existence_check = await Database().get_all_row_in_table_where_and(
        'youtube', 'channel_url', 'channel_url', 'user_id', message_text, user_id
    )
    if channel_name == False:
        await message.answer('Такого канала не существует!')
        await state.finish()
    else:
        if url_user_existence_check:
            await message.answer('Уведомления о этом канале уже включены')
        else:
            if not await Database().existance_check_user_id(user_id, 'notification_status'):
                await Database().sql_notification_status_add('ON', user_id)
            channel_name = await channel_name_corrector(channel_name)
            await message.answer(f'Уведомления о канале "{channel_name}" включены!')
            await Database().sql_youtube_add(channel_name, message_text, await youtube_url.parse_videos(message_text),
                                             user_id)
        await state.finish()


def get_keyboard_delete_youtube_channel(data):
    print(data)
    markup = InlineKeyboardMarkup()  # создаём клавиатуру
    markup.row_width = 1  # кол-во кнопок в строке
    for i in data:  # цикл для создания кнопок
        markup.add(InlineKeyboardButton(i[0],
                                        callback_data=f'del {i[0]}'))  # Создаём кнопки, i[1] - название, i[2] - каллбек дата
    return markup  # возвращаем клавиатуру


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def delete_callback_execute(callback_query: types.CallbackQuery):
    callback_query.data = callback_query.data.replace('del ', '')
    await Database().sql_remove_where_and(
        'youtube', 'channel_name', 'user_id', callback_query.data, callback_query.from_user.id)
    await callback_query.answer(text=f'Уведомления о канале "{callback_query.data}" выключены')
    # await bot.send_message(callback_query.from_user.id, f'Уведомления о канале "{callback_query.data}" выключены',)
    data = await Database().get_all_row_in_table_where('youtube', 'channel_name', 'user_id',
                                                       callback_query.from_user.id)
    await callback_query.message.edit_text(
        text='Какой канал удалить?', reply_markup=get_keyboard_delete_youtube_channel(data))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('upd '))
async def update_youtube_notification_status(call: types.CallbackQuery):
    status = {'ON': 'выключены', 'OFF': 'включены'}
    send_sql_status = {'ON': 'OFF', 'OFF': 'ON'}
    call_data = call.data.replace('upd ', '')
    await Database().sql_update('notification_status', 'youtube', 'user_id', send_sql_status[call_data],
                                str(call.from_user.id))
    await call.answer(text=f'Youtube уведомления "{status[call_data]}"')
    notification_status = await Database().get_all_row_in_table_where(
        'notification_status', 'youtube', 'user_id', str(call.from_user.id))
    await call.message.edit_text(text=f'Youtube уведомления "{status[call_data]}"')


async def delete_youtube_channel(message: types.Message):
    data = await Database().get_all_row_in_table_where('youtube', 'channel_name', 'user_id', message.from_user.id)
    if data:
        await message.answer('Какой канал удалить?', reply_markup=get_keyboard_delete_youtube_channel(data))
    else:
        await message.answer('У тебя ещё нету отслеживаемых каналов, ты можешь добаить их командой "/Добавить канал"')


def get_keyboard_youtube_notifications_setting(notification_status):
    status = {'ON': 'Выключить', 'OFF': 'Включить'}
    markup = InlineKeyboardMarkup()  # создаём клавиатуру
    markup.row_width = 1  # кол-во кнопок в строке
    markup.add(InlineKeyboardButton(
        f'{status[notification_status[0][0]]} уведомления', callback_data=f'upd {notification_status[0][0]}'))
    return markup


async def notification_youtube_setting(message: types.Message):
    notification_status = await Database().get_all_row_in_table_where(
        'notification_status', 'youtube', 'user_id', str(message.from_user.id))
    await message.answer('Что сделать с уведомлениями?',
                         reply_markup=get_keyboard_youtube_notifications_setting(notification_status))

"""


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(add_youtube_channel, text_contains=['Добавить канал'])
    #dp.register_message_handler(add_youtube_channel_set, state=youtube_states.AddChannel.set_channel)
    #dp.register_message_handler(delete_youtube_channel, text_contains=['Удалить канал'])
    #dp.register_message_handler(notification_youtube_setting, text_contains=['Настройка уведомлений'])


