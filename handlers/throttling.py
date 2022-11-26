from create_bot import _
from middlewares.i18m_language import get_user_locale


async def large_numbers_requests(*args, **kwargs):
    print(args)
    message = args[0]
    user_id = message.from_user.id
    try:
        await message.message.edit_text(_("Превышено количество запросов, попробуй позже",
                                          locale=await get_user_locale(user_id)))
    except:
        pass


async def throttling_alert(*args, **kwargs):
    message = args[0]
    user_id = message.from_user.id
    try:
        await message.answer(_("Не так часто! Попробуй немного позже", locale=await get_user_locale(user_id)))
    except:
        pass

