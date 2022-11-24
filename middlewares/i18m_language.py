from data_base.sqlite_db import User


async def get_user_locale(user_id):
    user_lang = await User.Language.get_language(user_id)
    return user_lang
