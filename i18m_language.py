from data_base.sqlite_db import Database


async def get_user_locale(user_id):
    """
    user_language = await Database().get_all_row_in_table_where('account', 'language', 'user_id', user_id)
    return user_language[0][0]
    """
    return 'ru'