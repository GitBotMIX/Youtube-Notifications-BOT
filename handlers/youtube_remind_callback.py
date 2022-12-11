import asyncio
import datetime
from aiogram import types, Dispatcher
from keyboards.markups import get_youtube_add_method_kb
from create_bot import _
from keyboards.remind_inline import get_youtube_remind_preview_kb, get_youtube_remind_kb, get_choose_day_kb, \
    get_choose_time_minutes_kb, get_choose_time_hours_kb, get_final_time_kb
from data_base.sqlite_db import Remind, User
from aiogram.utils.exceptions import MessageToDeleteNotFound
from functions.date_corrector import get_time_with_timezone


async def youtube_remind_delete_or_edit(call: types.CallbackQuery):
    user_id = call.from_user.id
    call_data = call.data.replace('youtube_remind_delete_or_edit ', '').split(':')
    video_url = call_data[0]
    user_lang = call_data[1]
    operation = call_data[2]
    await call.message.delete()
    if operation == 'edit':
        await call.message.answer(call.message.text, reply_markup=await get_youtube_remind_kb(user_id,
                                                                                              user_lang))
    else:
        button_text = _('Установить напоминание', locale=user_lang)
        await call.message.answer(call.message.text,
                                  reply_markup=await get_youtube_remind_preview_kb(user_id, button_text=button_text,
                                                                                   user_lang=user_lang))
        # await Remind.VideoUrl.delete(video_url, user_id=user_id)


async def choose_time_minutes_kb_full(call: types.CallbackQuery):
    call_data = call.data.replace('choose_time_minutes_kb_full ', '').split(':')
    day = call_data[0]
    hour = call_data[1]
    user_lang = call_data[2]
    await call.message.edit_text(call.message.text,
                                 reply_markup=await get_choose_time_minutes_kb(user_id=call.from_user.id,
                                                                               day=day, hour=hour, user_lang=user_lang,
                                                                               full_kb=True))


async def youtube_remind_day(call: types.CallbackQuery):
    call_data_list = call.data.replace('youtube_remind_day ', '').split(':')
    selected_day = call_data_list[0]
    user_lang = call_data_list[1]
    await call.message.edit_text(call.message.text,
                                 reply_markup=await get_choose_time_hours_kb(user_id=call.from_user.id,
                                                                             day=selected_day,
                                                                             user_lang=user_lang))


async def youtube_remind_kb(call: types.CallbackQuery):
    user_lang = call.data.replace('youtube_remind_kb ', '')
    await call.message.edit_text(call.message.text, reply_markup=await get_youtube_remind_kb(user_id=call.from_user.id,
                                                                                             user_lang=user_lang))


async def youtube_remind_date(call: types.CallbackQuery):
    user_id = call.from_user.id
    call_data_list = call.data.replace('youtube_remind_date ', '').split(':')
    remind_date = call_data_list[0]
    user_lang = call_data_list[1]
    user_timezone = await User.Timezone.where_user(user_id)
    user_timezone_math_sign = user_timezone[0][0]
    user_timezone_value = user_timezone[0][1:]
    day_map = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday',
               7: 'monday'}

    time_with_timezone = await get_time_with_timezone(user_timezone_math_sign, user_timezone_value)
    current_day = time_with_timezone.weekday()
    if remind_date == 'today':
        await call.message.edit_text(call.message.text, reply_markup=await get_choose_time_hours_kb(
            user_id=user_id,
            day='today',
            user_lang=user_lang))
    if remind_date == 'tomorrow':
        await call.message.edit_text(call.message.text, reply_markup=await get_choose_time_hours_kb(
            user_id=user_id,
            day=day_map[int(current_day) + 1],
            user_lang=user_lang))
    if remind_date == 'unknown':
        button_text = _('Установить напоминание', locale=user_lang)
        await call.message.edit_text(call.message.text, reply_markup=await get_youtube_remind_preview_kb(
            user_id=user_id,
            button_text=button_text,
            user_lang=user_lang))
    if remind_date == 'choose':
        await call.message.edit_text(call.message.text, reply_markup=await get_choose_day_kb(
            user_id=user_id,
            user_lang=user_lang))


async def get_next_weekday(current_date: datetime.date, weekday: int) -> datetime:
    days_ahead = weekday - current_date.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return current_date + datetime.timedelta(days_ahead)


async def youtube_remind_time_minutes(call: types.CallbackQuery):
    call_data_list = call.data.replace('YRT_minutes ', '').split(':')
    day_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
    user_id = call.from_user.id
    selected_day = call_data_list[0]
    selected_hours = call_data_list[1]
    selected_minutes = call_data_list[2]
    user_lang = call_data_list[3]
    message_text = call.message.text
    video_url = message_text[message_text.index("?v=") + 3:]

    user_timezone = await User.Timezone.where_user(user_id)
    user_timezone_math_sign = user_timezone[0][0]
    user_timezone_value = user_timezone[0][1:]

    date_now = await get_time_with_timezone(user_timezone_math_sign, user_timezone_value)

    if selected_day != 'today':
        next_weekday = await get_next_weekday(date_now.date(),
                                              day_map[selected_day])  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    else:
        next_weekday = date_now.date()
    remind_job_time = f'{next_weekday.day}-{selected_hours}-{selected_minutes}'

    await call.message.edit_text(call.message.text, reply_markup=await get_final_time_kb(
        user_id,
        next_weekday,
        selected_hours,
        selected_minutes,
        video_url,
        user_lang))
    await asyncio.sleep(30)
    try:
        await call.message.delete()
        await Remind.add(video_url, remind_job_time, user_id)
    except MessageToDeleteNotFound:
        pass


async def youtube_remind_time_hours(call: types.CallbackQuery):
    call_data_list = call.data.replace('youtube_remind_time_hours ', '').split(':')
    selected_time_hours = call_data_list[0]
    selected_day = call_data_list[1]
    user_lang = call_data_list[2]
    await call.message.edit_text(call.message.text, reply_markup=await get_choose_time_minutes_kb(call.from_user.id,
                                                                                                  selected_day,
                                                                                                  selected_time_hours,
                                                                                                  user_lang))


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(youtube_remind_kb,
                                       lambda x: x.data and x.data.startswith('youtube_remind_kb'))
    dp.register_callback_query_handler(youtube_remind_date,
                                       lambda x: x.data and x.data.startswith('youtube_remind_date'))
    dp.register_callback_query_handler(youtube_remind_day,
                                       lambda x: x.data and x.data.startswith('youtube_remind_day'))
    dp.register_callback_query_handler(youtube_remind_time_hours,
                                       lambda x: x.data and x.data.startswith('youtube_remind_time_hours'))
    dp.register_callback_query_handler(youtube_remind_time_minutes,
                                       lambda x: x.data and x.data.startswith('YRT_minutes'))
    dp.register_callback_query_handler(choose_time_minutes_kb_full,
                                       lambda x: x.data and x.data.startswith('choose_time_minutes_kb_full'))
    dp.register_callback_query_handler(youtube_remind_delete_or_edit,
                                       lambda x: x.data and x.data.startswith('youtube_remind_delete_or_edit'))
