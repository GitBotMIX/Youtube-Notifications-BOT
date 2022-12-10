from middlewares.i18m_language import get_user_locale
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_timezone_kb(user_id: str | int, user_lang=None) -> InlineKeyboardMarkup:
    user_lang = (await get_user_locale(user_id) if not user_lang else user_lang)
    timezone_kb = InlineKeyboardMarkup(resize_keyboard=False)
    timezone_kb.row_width = 4
    button_list_display = []
    button_list_backend = []
    for i in range(-13, 15):
        if i >= 10 or i <= -10:
            if i >= 10:
                display = f'+{i}:00'
            else:
                display = f'{i}:00'
        else:
            if i < 0:
                display = f'{str(i)[0]}0{str(i)[1]}:00'
            else:
                display = f'+0{i}:00'
        button_list_display.append(display)
        button_list_backend.append(i)
    timezone_kb.add(*[InlineKeyboardButton(
        f'{timezone}',
        callback_data=f'select_timezone {button_list_backend[i]}:{timezone}:{user_lang}')
        for i, timezone in enumerate(button_list_display)])
    return timezone_kb
