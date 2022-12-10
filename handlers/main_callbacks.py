from create_bot import _
from aiogram import types, Dispatcher
from data_base.sqlite_db import User
from keyboards.timezone_inline import get_timezone_kb
import aiogram.utils.markdown as fmt


async def none_answer(call: types.CallbackQuery):
    none_answer_text = call.data.replace('none_answer ', '')
    await call.answer(none_answer_text)


async def set_user_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_lang = call.data.replace('set_user_language ', '')
    wiki_site_url = 'https://en.wikipedia.org/wiki/List_of_time_zones_by_country'
    if user_lang == 'ru':
        wiki_site_url = 'https://ru.wikipedia.org/wiki/Список_часовых_поясов_по_странам'
    await User.Language.update(user_lang, user_id)
    await call.message.edit_text(_('🌍 Теперь необходимо определиться с часовым поясом. '
                                   'Укажи разницу во времени относительно UTC.\n'
                                   '{}', locale=user_lang).format(fmt.hide_link(wiki_site_url)),
                                 reply_markup=await get_timezone_kb(user_id, user_lang),
                                 parse_mode=types.ParseMode.HTML)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(none_answer,
                                       lambda x: x.data and x.data.startswith('none_answer'))
    dp.register_callback_query_handler(set_user_language,
                                       lambda x: x.data and x.data.startswith('set_user_language'))
