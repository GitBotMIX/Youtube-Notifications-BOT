from youtubesearchpython.__future__ import ChannelsSearch, Video
import asyncio
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.i18m_language import get_user_locale
from create_bot import _
from keyboards.markups import get_youtube_add_method_kb
from functions import youtube_url
from data_base.sqlite_db import Youtube
from states.youtube_states import AddChannel
from aiogram.utils.exceptions import Throttled
from handlers.throttling import large_numbers_requests, throttling_alert


async def notifications_enabled(user_id, user_lang, channel_name):
    send_message_data = await bot.send_message(user_id, '✔')
    await asyncio.sleep(1.2)
    await bot.edit_message_text(
        _('🔔Уведомления о канале "{}" включены✔', locale=user_lang).format(channel_name),
        chat_id=user_id, message_id=send_message_data.message_id)


async def notifications_enabled_error(user_id, user_lang, channel_name):
    send_message_data = await bot.send_message(user_id, '❌')
    await asyncio.sleep(1.2)
    await bot.edit_message_text(
        _('Уведомления о канале "{}" уже включены❌', locale=user_lang).format(channel_name),
        chat_id=user_id, message_id=send_message_data.message_id)


@dp.throttled(throttling_alert, rate=3)
async def add_youtube_channel(message: types.Message, user_lang):
    user_id = message.from_user.id
    name_and_url_channel_list = await Youtube.Channel.get_all_rows_related_id(user_id)
    if len(name_and_url_channel_list) >= 4:
        await message.answer(_('У тебя слишком много каналов.\nЧто-бы добавить новые - удали старые:', locale=user_lang),
                             reply_markup=await get_delete_youtube_channel_kb(name_and_url_channel_list))
    else:
        await message.answer(_('Выбери метод поиска канала🔍', locale=user_lang),
                             reply_markup=await get_youtube_add_method_kb(user_id))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('youtube_add_method '))
@dp.throttled(large_numbers_requests, rate=4)
async def youtube_add_method_call_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_lang = await get_user_locale(user_id)
    add_method = call.data.replace('youtube_add_method ', '')
    if add_method == 'channel_name':
        await call.message.edit_text(_('🔍Введи название канала:', locale=user_lang))
        await AddChannel.channel_name.set()
    elif add_method == 'channel_url':
        await call.message.edit_text(_('🕹Введи ссылку на канал:', locale=user_lang))
        await AddChannel.channel_url.set()
    elif add_method == 'channel_video_url':
        await call.message.edit_text(_('🎥Введи ссылку на видео с канала:', locale=user_lang))
        await AddChannel.channel_video_url.set()
    else:
        await call.message.edit_text(_('Как я работаю❓\n'
                                       'Для начала нужно добавить канал, '
                                       'что-бы это сделать нажми на кнопку "Добавить канал", '
                                       'затем выбери метод которым ты будешь добавлять канал:\n\n'
                                       'По названию канала - просто введи название нужного тебе канала.\n\n'
                                       'По ссылке на канал - для того что-бы получить ссылку на канал, '
                                       'зайди в ютубе на главную страницу нужного тебе канала, дальше либо скопируй '
                                       'ссылку с адресной строки браузера, либо если ты открыл канал в приложении '
                                       'нажми на 3 точки в правом верхнем углу, затем "Поделиться", нажми на кнопку '
                                       '"Скопировать ссылку", осталось только отправить эту ссылку боту после нажатия '
                                       'соответствующей кнопки.\n\n'
                                       'По ссылке на видео с канала - что-бы получить ссылку на видео с канала, '
                                       'нужно открыть любое видео с нужного тебе канала, затем нажми на кнопку '
                                       '"Поделиться" и "Скопировать ссылку", дальше осталось только отправить '
                                       'эту ссылку боту, после нажатия соответствующей кнопки.', locale=user_lang))


async def get_is_channel_correct_kb(channel_url: str, user_request_channel_name: str,
                                    channel_number: int, user_lang: str):
    channel_id = '/'.join(channel_url.split('/')[3:])
    user_request_channel_name = user_request_channel_name[:20]
    b1 = InlineKeyboardButton(text=_('Да', locale=user_lang),  # YRC youtube_right_channel
                              callback_data=f"YRC {channel_id}")
    b2 = InlineKeyboardButton(text=_('Нет', locale=user_lang),  # YWC youtube_wrong_channel
                              callback_data=f'YWC {user_request_channel_name}:{str(channel_number)}')
    b3 = InlineKeyboardButton(text=_('Ссылка на канал', locale=user_lang),
                              url=channel_url)
    channel_correct_kb = InlineKeyboardMarkup(resize_keyboard=False)
    return channel_correct_kb.row(b1, b2).add(b3)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('YRC '))
async def youtube_right_channel_call_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_lang = await get_user_locale(user_id)
    channel_short_url = call.data.replace('YRC ', '')
    channel_url = await youtube_url.get_channel_url_by_short_url(channel_short_url)
    channel_name = await youtube_url.get_channel_title(channel_url)
    current_video = await youtube_url.parse_videos(channel_url)
    user_channels_url_list = await Youtube.Channel.Url.where_user(user_id)
    if channel_url not in user_channels_url_list:
        await call.message.edit_text('✔')
        await asyncio.sleep(1.5)
        await call.message.edit_text(_('🔔Уведомления о канале "{}" включены✔', locale=user_lang).format(channel_name))
        await Youtube.add(channel_name, channel_url, current_video, user_id)
    else:
        await call.message.edit_text('❌')
        await asyncio.sleep(1.5)
        await call.message.edit_text(
            _('Уведомления о канале "{}" уже включены❌', locale=user_lang).format(channel_name))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('YWC '))
async def youtube_wrong_channel_call_handler(call: types.CallbackQuery):
    data_list = call.data.replace('YWC ', '').split(':')
    user_id = call.from_user.id
    user_lang = await get_user_locale(user_id)
    search_name = data_list[0]
    channel_number = int(data_list[1])
    channel_number += 1
    message_id = call.message.message_id
    await YoutubeSearch.with_channel_name(call, search_name, user_id, user_lang, message_id,
                                          channel_number=int(channel_number), is_callback=True)


class YoutubeSearch:
    @staticmethod
    async def with_channel_name_call():
        pass

    @staticmethod
    async def with_channel_name_message():
        pass

    @staticmethod
    async def with_channel_name(message: types.Message | types.CallbackQuery,
                                search_name: str, user_id: int,
                                user_lang: str, message_id: int,
                                call_count: int = 0,
                                channel_number: int = 0,
                                bot_msg=None, is_callback=None):
        call_count += 1
        channel_number_limit = 10
        if channel_number == channel_number_limit:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                        text=_('Не удается найти нужный канал, попробуй ввести более '
                                               'точное название канала, либо используй другой метод '
                                               'добавления канала', locale=user_lang),
                                        reply_markup=await get_youtube_add_method_kb(user_id))
            return
        if call_count >= 15:
            await bot.delete_message(user_id, bot_msg.message_id)
            await bot.send_message(user_id, _('Не могу найти информацию о канале "{}"\n '
                                              'Попробуй ещё раз!', locale=user_lang).format(search_name),
                                   reply_markup=await get_youtube_add_method_kb(user_id))
            return
        channel_search = await ChannelsSearch(search_name, limit=channel_number_limit).next()
        try:
            video_count = channel_search['result'][channel_number]['videoCount']
            channel_subs = channel_search['result'][channel_number]['subscribers'][:-11]
        except IndexError:
            await bot.send_message(user_id,
                                   _('Не могу найти канал с именем "{}"', locale=user_lang).format(search_name))
            return
        except TypeError:
            await YoutubeSearch.with_channel_name(message, search_name, user_id, user_lang, message_id, call_count,
                                                  channel_number + 1, bot_msg, is_callback)
            return
        if not video_count or not channel_subs:
            await asyncio.sleep(0.2)
            call_count_animation = {1: '🔍', 7: '🔎'}
            if not is_callback:
                if call_count == 1:
                    bot_msg = await bot.send_message(user_id, _('...', locale=user_lang))
                try:
                    await bot.edit_message_text(chat_id=user_id, message_id=bot_msg.message_id,
                                                text=call_count_animation[call_count])
                except KeyError:
                    pass
                except AttributeError:
                    pass
            await YoutubeSearch.with_channel_name(message, search_name, user_id, user_lang, message_id, call_count,
                                                  channel_number, bot_msg, is_callback)
            return
        try:
            await bot.delete_message(user_id, bot_msg.message_id)
        except AttributeError:
            pass
        channel_url = channel_search['result'][channel_number]['link']
        channel_logo_url = f"{'https:'}{channel_search['result'][channel_number]['thumbnails'][1]['url']}"
        response_text = _('*Этот канал ты ищешь?*\n\n'
                          'Название: *{channel_name}*\n'
                          'Подписчики: *{channel_subs}*\n'
                          'Всего видео: *{channel_video_count}*'
                          '{channel_logo_url}', locale=user_lang).format(
            channel_name=channel_search['result'][channel_number]['title'],
            channel_subs=channel_subs,
            channel_video_count=video_count,
            channel_logo_url=f"[.]({channel_logo_url})")
        if is_callback:
            await message.message.edit_text(response_text, parse_mode='Markdown',
                                            reply_markup=await get_is_channel_correct_kb(channel_url, search_name,
                                                                                         channel_number, user_lang))
        else:
            await bot.send_message(user_id, response_text, parse_mode='Markdown',
                                   reply_markup=await get_is_channel_correct_kb(channel_url, search_name,
                                                                                channel_number, user_lang))
            # await bot.send_photo(user_id, photo=channel_logo_url, caption=response_text, parse_mode='Markdown',
            #                     reply_markup=await get_is_channel_correct_kb(channel_url, search_name,
            #                                                                  channel_number, user_lang))


async def youtube_add_with_channel_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = await get_user_locale(user_id)
    search_name = message.text
    channel_number = 0
    message_id = message.message_id
    await YoutubeSearch.with_channel_name(message, search_name, user_id, user_lang, message_id,
                                          channel_number=int(channel_number))

    await state.finish()


async def youtube_add_with_channel_url(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = await get_user_locale(user_id)
    try:
        channel_url = await youtube_url.get_channel_url_id_by_url(message.text)
    except:
        send_message_data = await bot.send_message(user_id, '❌')
        await asyncio.sleep(1.2)
        await bot.edit_message_text(_('Введена неверная ссылка на канал❌', locale=user_lang), chat_id=user_id,
                                    message_id=send_message_data.message_id)
        await state.finish()
        return
    channel_name = await youtube_url.get_channel_title(channel_url)
    current_video = await youtube_url.parse_videos(channel_url)
    user_channels_url_list = await Youtube.Channel.Url.where_user(user_id)
    if channel_url not in user_channels_url_list:
        await notifications_enabled(user_id, user_lang, channel_name)
        await Youtube.add(channel_name, channel_url, current_video, user_id)
    else:
        await notifications_enabled_error(user_id, user_lang, channel_name)
    await state.finish()


async def youtube_add_with_channel_video_url(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = await get_user_locale(user_id)
    user_video_url = message.text
    try:
        video = await Video.getInfo(user_video_url)
    except:  # TypeError or ValueError
        send_message_data = await bot.send_message(user_id, '❌')
        await asyncio.sleep(1.2)
        await bot.edit_message_text(_('Не могу найти видео по твоей ссылке.❌\n'
                                      'Пример правильной ссылки на видео с канала '
                                      '- https://www.youtube.com/watch?v=ycPr5-27vSI', locale=user_lang),
                                    chat_id=user_id, message_id=send_message_data.message_id,
                                    disable_web_page_preview=True)
        await state.finish()
        return
    response_channel_name = video["channel"]['name']
    response_channel_url = video["channel"]['link']
    current_video = await youtube_url.parse_videos(response_channel_url)
    user_channels_url_list = await Youtube.Channel.Url.where_user(user_id)
    if response_channel_url not in user_channels_url_list:
        await notifications_enabled(user_id, user_lang, response_channel_name)
        await Youtube.add(response_channel_name, response_channel_url, current_video, user_id)
    else:
        await notifications_enabled_error(user_id, user_lang, response_channel_name)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def delete_callback_execute(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_lang = await get_user_locale(user_id)
    channel_url = call.data.replace('del ', '')
    await Youtube.Channel.Url.delete(channel_url, user_id)
    await call.answer(text=_('Уведомления о канале выключены', locale=user_lang))
    name_and_url_channel_list = await Youtube.Channel.get_all_rows_related_id(user_id)
    if name_and_url_channel_list:
        await call.message.edit_text(
            text=_('Какой канал удалить?', locale=user_lang),
            reply_markup=await get_delete_youtube_channel_kb(name_and_url_channel_list))
    else:
        await call.message.edit_text(text=_('Все каналы удалены✖', locale=user_lang))


async def get_delete_youtube_channel_kb(name_and_url_channel_list):
    markup = InlineKeyboardMarkup()  # создаём клавиатуру
    markup.row_width = 1  # кол-во кнопок в строке
    for i in name_and_url_channel_list:  # цикл для создания кнопок
        markup.add(InlineKeyboardButton(i[0][:20],
                                        callback_data=f'del {i[1]}'))
    return markup  # возвращаем клавиатуру


@dp.throttled(throttling_alert, rate=6)
async def delete_youtube_channel(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_locale(user_id)
    name_and_url_channel_list = await Youtube.Channel.get_all_rows_related_id(user_id)
    if name_and_url_channel_list:
        await message.answer(_('Какой канал удалить?', locale=user_lang),
                             reply_markup=await get_delete_youtube_channel_kb(name_and_url_channel_list))
    else:
        await message.answer(_('❌У тебя ещё нету отслеживаемых каналов, ты можешь добавить их командой '
                               '"Добавить канал"',
                               locale=user_lang))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(add_youtube_channel,
                                lambda msg: any(i in msg.text.lower() for i in ['добавить канал', 'add channel']))
    dp.register_message_handler(youtube_add_with_channel_name, state=AddChannel.channel_name)
    dp.register_message_handler(youtube_add_with_channel_url, state=AddChannel.channel_url)
    dp.register_message_handler(youtube_add_with_channel_video_url, state=AddChannel.channel_video_url)
    dp.register_message_handler(delete_youtube_channel,
                                lambda msg: any(i in msg.text.lower() for i in ['удалить канал', 'delete channel']))
