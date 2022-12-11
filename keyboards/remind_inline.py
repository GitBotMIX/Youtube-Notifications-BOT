from middlewares.i18m_language import get_user_locale
from create_bot import _
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base.sqlite_db import User
from functions.date_corrector import get_time_with_timezone
from datetime import datetime, timezone, timedelta


async def get_final_time_kb(user_id: str | int, next_weekday: int, hour: str, minutes: str, video_url: str,
                            user_lang=None) -> InlineKeyboardMarkup:
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    full_time = f'{str(next_weekday)} | {hour}:{minutes}'
    remind_text = _('Напоминание установлено на {}', locale=user_lang).format(full_time)
    b1 = InlineKeyboardButton(text=remind_text,
                              callback_data=f'none_answer {full_time}')
    b2 = InlineKeyboardButton(text=_('Удалить', locale=user_lang),
                              callback_data=f'youtube_remind_delete_or_edit {video_url}:{user_lang}:delete')
    b3 = InlineKeyboardButton(text=_('Изменить', locale=user_lang),
                              callback_data=f'youtube_remind_delete_or_edit {video_url}:{user_lang}:edit')
    final_time_kb = InlineKeyboardMarkup(resize_keyboard=False)
    return final_time_kb.add(b1).row(b2, b3)


async def get_choose_time_minutes_kb(user_id: str | int, day: str, hour: str, user_lang=None, full_kb=None) \
        -> InlineKeyboardMarkup:
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    choose_time_minutes_kb = InlineKeyboardMarkup(resize_keyboard=False)
    b1 = InlineKeyboardButton(text='...',
                              callback_data=f'choose_time_minutes_kb_full {day}:{hour}:{user_lang}')
    choose_time_minutes_kb.row_width = 4
    button_list = []
    min_minute = 0
    user_timezone = await User.Timezone.where_user(user_id)
    user_timezone_math_sign = user_timezone[0][0]
    user_timezone_value = user_timezone[0][1:]

    date_now = await get_time_with_timezone(user_timezone_math_sign, user_timezone_value)
    step = 5
    if full_kb:
        step = 1
        choose_time_minutes_kb.row_width = 5
    if day == 'today' and hour == str(date_now.hour):
        min_minute = int(date_now.minute) + 5
    for i in range(min_minute, 60, step):
        if i >= 10:
            s = f'{hour}:{i}'
        else:
            s = f'{hour}:0{i}'
        button_list.append(s)
    choose_time_minutes_kb.add(*[InlineKeyboardButton(
        f'{time}',
        callback_data=f'YRT_minutes {day}:{hour}:{time[-2:]}:{user_lang}')
        for time in button_list])
    if full_kb:
        return choose_time_minutes_kb
    else:
        return choose_time_minutes_kb.add(b1)


async def get_choose_time_hours_kb(user_id: str | int, day: str, user_lang=None) -> InlineKeyboardMarkup:
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    choose_time_hours_kb = InlineKeyboardMarkup(resize_keyboard=False)
    choose_time_hours_kb.row_width = 4
    button_list = []
    min_hour = 0
    user_timezone = await User.Timezone.where_user(user_id)
    user_timezone_math_sign = user_timezone[0][0]
    user_timezone_value = user_timezone[0][1:]

    time_with_timezone = await get_time_with_timezone(user_timezone_math_sign, user_timezone_value)

    if day == 'today':
        min_hour = int(time_with_timezone.hour)
    for i in range(min_hour, 24):
        if i >= 10:
            s = f'{i}:00'
        else:
            s = f'0{i}:00'
        button_list.append(s)
    choose_time_hours_kb.add(*[InlineKeyboardButton(
        f'{time}',
        callback_data=f'youtube_remind_time_hours {time[:2]}:{day}:{user_lang}')
        for time in button_list])
    return choose_time_hours_kb


async def get_choose_day_kb(user_id, user_lang=None) -> InlineKeyboardMarkup:
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    user_timezone = await User.Timezone.where_user(user_id)
    user_timezone_math_sign = user_timezone[0][0]
    user_timezone_value = user_timezone[0][1:]
    day_map_en = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday',
                  4: 'friday', 5: 'saturday', 6: 'sunday', 7: 'monday'}
    day_map_ru = {0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг',
                  4: 'пятница', 5: 'суббота', 6: 'воскресенье', 7: 'понедельник'}
    if user_lang == 'ru':
        day_map = day_map_ru
    else:
        day_map = day_map_en

    time_with_timezone = await get_time_with_timezone(user_timezone_math_sign, user_timezone_value)

    b0 = InlineKeyboardButton(text=_('Сегодня - {}', locale=user_lang).format(
        day_map[time_with_timezone.weekday()].title()),
        callback_data=f'youtube_remind_date today:{user_lang}')
    b1 = InlineKeyboardButton(text=_('Понедельник', locale=user_lang),
                              callback_data=f'youtube_remind_day monday:{user_lang}')
    b2 = InlineKeyboardButton(text=_('Вторник', locale=user_lang),
                              callback_data=f'youtube_remind_day tuesday:{user_lang}')
    b3 = InlineKeyboardButton(text=_('Среда', locale=user_lang),
                              callback_data=f'youtube_remind_day wednesday:{user_lang}')
    b4 = InlineKeyboardButton(text=_('Четверг', locale=user_lang),
                              callback_data=f'youtube_remind_day thursday:{user_lang}')
    b5 = InlineKeyboardButton(text=_('Пятница', locale=user_lang),
                              callback_data=f'youtube_remind_day friday:{user_lang}')
    b6 = InlineKeyboardButton(text=_('Суббота', locale=user_lang),
                              callback_data=f'youtube_remind_day saturday:{user_lang}')
    b7 = InlineKeyboardButton(text=_('Воскресенье', locale=user_lang),
                              callback_data=f'youtube_remind_day sunday:{user_lang}')
    choose_day_kb = InlineKeyboardMarkup(resize_keyboard=False)
    return choose_day_kb.add(b0).row(b1, b2, b3).row(b4, b5, b6).add(b7)


async def get_youtube_remind_preview_kb(user_id, button_text: str, user_lang=None) \
        -> InlineKeyboardMarkup:
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    b1 = InlineKeyboardButton(text=button_text,
                              callback_data=f'youtube_remind_kb {user_lang}')
    youtube_remind_preview_kb = InlineKeyboardMarkup(resize_keyboard=False)
    return youtube_remind_preview_kb.add(b1)


async def get_youtube_remind_kb(user_id, user_lang=None) -> InlineKeyboardMarkup:
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    b1 = InlineKeyboardButton(text=_('Сегодня', locale=user_lang),
                              callback_data=f'youtube_remind_date today:{user_lang}')
    b2 = InlineKeyboardButton(text=_('Завтра', locale=user_lang),
                              callback_data=f'youtube_remind_date tomorrow:{user_lang}')
    b3 = InlineKeyboardButton(text=_('...', locale=user_lang),
                              callback_data=f'youtube_remind_date choose:{user_lang}')
    b4 = InlineKeyboardButton(text=_('Отменить', locale=user_lang),
                              callback_data=f'youtube_remind_date unknown:{user_lang}')
    # b5 = InlineKeyboardButton(text=_('Как в прошлый раз', locale=user_lang),
    #                           callback_data=f'youtube_remind_date unknown:{user_lang}')
    youtube_remind_kb = InlineKeyboardMarkup(resize_keyboard=False)
    return youtube_remind_kb.row(b1, b2, b3).add(b4)
