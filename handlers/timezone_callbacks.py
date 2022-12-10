import asyncio
import datetime
from aiogram import types, Dispatcher
from keyboards.markups import get_youtube_add_method_kb
from create_bot import _
from keyboards.remind_inline import get_youtube_remind_preview_kb, get_youtube_remind_kb, get_choose_day_kb, \
    get_choose_time_minutes_kb, get_choose_time_hours_kb, get_final_time_kb
from data_base.sqlite_db import Remind, User
from keyboards.youtube_main_kb import get_youtube_main_kb


async def select_timezone(call: types.CallbackQuery):
    user_id = call.from_user.id
    call_data = call.data.replace('select_timezone ', '').split(':')
    timezone = call_data[0]
    timezone_display = f"{call_data[1]:{call_data[2]}}"
    user_lang = call_data[3]
    send_msg = await call.message.edit_text(_('⏱Часовой пояс установлен✔', locale=user_lang).format(timezone_display))
    await asyncio.sleep(2)
    await call.message.delete()
    await asyncio.sleep(0.3)
    await call.message.answer(_('Отлично, теперь наконец-то можно пользоваться функциями бота, '
                                'для этого используй меню бота.', locale=user_lang),
                              reply_markup=await get_youtube_main_kb(user_id, user_lang))
    if int(timezone) >= 0:
        timezone = f'+{timezone}'
    await User.Timezone.update(timezone, user_id)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(select_timezone,
                                       lambda x: x.data and x.data.startswith('select_timezone'))
