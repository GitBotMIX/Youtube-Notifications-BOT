from create_bot import _
from i18m_language import get_user_locale


async def large_numbers_requests(*args, **kwargs):
    message = args[0]
    user_id = message.from_user.id
    await message.answer(_("Превышено количество запросов, попробуй позже", locale=await get_user_locale(user_id)))
