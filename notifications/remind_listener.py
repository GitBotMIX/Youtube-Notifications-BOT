from data_base.sqlite_db import User, Remind
from datetime import datetime, timezone, timedelta
from create_bot import bot
from middlewares.i18m_language import get_user_locale
from create_bot import _
from keyboards.remind_inline import get_youtube_remind_preview_kb
from functions.date_corrector import get_time_with_timezone


async def send_remind_message(video_id, user_id, there_were_technical_problems: bool = None):
    user_lang = await get_user_locale(user_id)

    video_url = f'https://www.youtube.com/watch?v={video_id}'
    button_text = _('Напомнить позже', locale=user_lang)

    if there_were_technical_problems:
        message_text = _('🔔Напоминание о видео! \n⚠На сервере бота произошли технические неполадки, '
                         'просим прощения за задержку напоминания.\n{}', locale=user_lang).format(video_url)
    else:
        message_text = _('🔔Напоминание о видео!\n{}', locale=user_lang).format(video_url)
    await bot.send_message(user_id, message_text,
                           reply_markup=await get_youtube_remind_preview_kb(user_id,
                                                                            button_text=button_text,
                                                                            user_lang=user_lang))
    await Remind.VideoUrl.delete(video_id, user_id)


async def listen():
    all_remind_note: list[tuple[str]] = await Remind.get_all_rows()
    for remind_note in all_remind_note:
        user_id = remind_note[2]
        video_id = remind_note[0]
        remind_date = remind_note[1].split('-')
        remind_date_day = remind_date[0]
        remind_date_hour = remind_date[1]
        remind_date_minutes = remind_date[2]

        user_timezone = await User.Timezone.where_user(user_id)
        user_timezone_math_sign = user_timezone[0][0]
        user_timezone_value = user_timezone[0][1:]

        time_with_timezone = await get_time_with_timezone(user_timezone_math_sign, user_timezone_value)

        date_hour_with_timezone = time_with_timezone.hour
        date_day = time_with_timezone.day
        date_minutes = time_with_timezone.minute
        print(f'remind_date_hour = {remind_date_hour}')
        print(f'date_hour_with_timezone = {date_hour_with_timezone}')
        print(f'remind_date_day = {remind_date_day}')
        print(f'date_day = {date_day}')
        print(f'remind_date_minutes = {remind_date_minutes}')
        print(f'date_minutes = {date_minutes}')

        if int(remind_date_hour) <= date_hour_with_timezone:
            if int(remind_date_day) == date_day:
                if int(remind_date_minutes) == date_minutes:
                    await send_remind_message(video_id, user_id)
                if int(remind_date_minutes) < date_minutes:
                    await send_remind_message(video_id, user_id, there_were_technical_problems=True)
        else:
            if int(remind_date_day) < date_day:
                await send_remind_message(video_id, user_id, there_were_technical_problems=True)
