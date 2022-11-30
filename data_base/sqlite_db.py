import sqlite3 as sq
from constants import YOUTUBE_TABLE, YOUTUBE_ROWS, USER_TABLE, USER_ROWS


def sql_start():
    global cur, base
    base = sq.connect('Notifications.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute(f'CREATE TABLE IF NOT EXISTS user({USER_ROWS["STATUS"]} TEXT, {USER_ROWS["LANGUAGE"]} TEXT, '
                 f'{USER_ROWS["USER"]} TEXT)')
    base.execute(f'CREATE TABLE IF NOT EXISTS '
                 f'youtube({YOUTUBE_ROWS["CHANNEL_NAME"]} TEXT, {YOUTUBE_ROWS["URL"]} TEXT, '
                 f'{YOUTUBE_ROWS["VIDEO"]} TEXT, {YOUTUBE_ROWS["USER"]} TEXT)')
    base.commit()
    return cur, base


async def tuple_list_to_list_first_values_in_tuple(list_tuple: list[tuple]) -> list:
    list_values = [i[0] for i in list_tuple]
    return list_values


class Methods:
    SELECT_ROWS = None
    SELECT_ROW = None
    TABLE = None
    WHERE_ROW = None

    @classmethod
    async def get_all_rows_related_id(cls, user_id):
        if len(cls.SELECT_ROWS) == 1:
            __select_rows_str = cls.SELECT_ROWS[0]
        else:
            __select_rows_str = ','.join(cls.SELECT_ROWS)
        __tuple_list = cur.execute(f'SELECT {__select_rows_str} '
                                   f'FROM {cls.TABLE} '
                                   f'WHERE {cls.WHERE_ROW} == ?', (user_id,)).fetchall()
        return __tuple_list

    @classmethod
    async def where_user(cls, user_id):
        where_user_tuple_list = cur.execute(f'SELECT {cls.SELECT_ROW} '
                                            f'FROM {cls.TABLE} '
                                            f'WHERE {cls.WHERE_ROW} == ?', (user_id,)).fetchall()
        return await tuple_list_to_list_first_values_in_tuple(where_user_tuple_list)

    @classmethod
    async def get_all(cls):
        get_all_tuple_list = cur.execute(f'SELECT {cls.SELECT_ROW} '
                                         f'FROM {cls.TABLE}').fetchall()
        return await tuple_list_to_list_first_values_in_tuple(get_all_tuple_list)


class Database:
    @staticmethod
    async def sql_add(args: tuple, table_name):
        rows_value_str = '?, '
        cur.execute(f'INSERT INTO {table_name} VALUES ({(rows_value_str * len(args))[0:-2]})', args)
        base.commit()

    @staticmethod
    async def sql_delete(table_name: str, where: str, where_data: str, **and_data):
        if and_data:
            and_sql_str = [i[0] for i in and_data.items()]
            and_data_list = [str(i[1]) for i in and_data.items()]
            and_sql_generated_str = ''
            and_data_list.insert(0, str(where_data))
            for i in and_sql_str:
                and_sql_generated_str += f' AND {i} == ?'
            cur.execute(f'DELETE FROM {table_name} WHERE {where} == ?{and_sql_generated_str}',
                        tuple(and_data_list))
            base.commit()
        else:
            cur.execute(f'DELETE FROM {table_name} WHERE {where} == ?', str(where_data))
            base.commit()

    @staticmethod
    async def sql_update(table_name: str, set_row: str, set_row_data: str, where: str, where_data: str, **and_data):
        if and_data:
            and_sql_str = [i[0] for i in and_data.items()]
            and_data_list = [str(i[1]) for i in and_data.items()]
            and_sql_generated_str = ''
            and_data_list.insert(0, str(where_data))
            and_data_list.insert(0, str(set_row_data))
            for i in and_sql_str:
                and_sql_generated_str += f' AND {i} == ?'
            cur.execute(f'UPDATE {table_name} SET {set_row} == ? WHERE {where} == ?{and_sql_generated_str}',
                        tuple(and_data_list))
            base.commit()
        else:
            cur.execute(f'UPDATE {table_name} SET {set_row} == ? WHERE {where} == ?',
                        (str(set_row_data), str(where_data),))
            base.commit()


class User:
    @staticmethod
    async def add(*args: str):
        await Database().sql_add(args, USER_TABLE)

    @staticmethod
    async def delete(user_id: str):
        await Database().sql_delete(USER_TABLE, USER_ROWS['USER'], user_id)

    @staticmethod
    async def get_user(user_id):
        user_id_tuple_list = cur.execute(f'SELECT {USER_ROWS["USER"]} '
                                         f'FROM {USER_TABLE} '
                                         f'WHERE {USER_ROWS["USER"]} == ?', (str(user_id),)).fetchone()
        return user_id_tuple_list

    class Status(Methods):
        SELECT_ROW = USER_ROWS["STATUS"]
        TABLE = USER_TABLE
        WHERE_ROW = USER_ROWS["USER"]

        @staticmethod
        async def to_premium(user_id):
            user_id = str(user_id)
            cur.execute(f'UPDATE {USER_TABLE} SET {USER_ROWS["STATUS"]} == ? '
                        f'WHERE {USER_ROWS["USER"]} == ?', ('premium', user_id,))
            base.commit()

    class Language:
        SELECT_ROW = USER_ROWS["LANGUAGE"]
        TABLE = USER_TABLE
        WHERE_ROW = USER_ROWS["USER"]

        @staticmethod
        async def get_language(user_id):
            user_language_tuple_list = cur.execute(f'SELECT {USER_ROWS["LANGUAGE"]} '
                                                   f'FROM {USER_TABLE} '
                                                   f'WHERE {USER_ROWS["USER"]} == ?', (str(user_id),)).fetchone()
            return user_language_tuple_list[0]

        @classmethod
        async def update(cls, language: str, user_id: str | int):
            await Database.sql_update(cls.TABLE, cls.SELECT_ROW, language, cls.WHERE_ROW, str(user_id))

    class Id(Methods):
        SELECT_ROW = USER_ROWS["USER"]
        WHERE_ROW = USER_ROWS["USER"]
        TABLE = USER_TABLE


class Youtube(Methods):
    SELECT_ROWS = [YOUTUBE_ROWS["CHANNEL_NAME"], YOUTUBE_ROWS["URL"],
                   YOUTUBE_ROWS["VIDEO"], YOUTUBE_ROWS["USER"]]

    @staticmethod
    async def add(*args: str):
        await Database().sql_add(args, YOUTUBE_TABLE)

    @staticmethod
    async def delete(user_id: str | int):
        await Database().sql_delete(YOUTUBE_TABLE, YOUTUBE_ROWS['USER'], str(user_id))

    @staticmethod
    async def get_user(user_id):
        user_id_tuple_list = cur.execute(f'SELECT {YOUTUBE_ROWS["USER"]} '
                                         f'FROM {YOUTUBE_TABLE} '
                                         f'WHERE {YOUTUBE_ROWS["USER"]} == ?', (str(user_id),)).fetchone()
        return user_id_tuple_list

    class Channel(Methods):
        TABLE = YOUTUBE_TABLE
        SELECT_ROWS = [YOUTUBE_ROWS["CHANNEL_NAME"], YOUTUBE_ROWS["URL"], YOUTUBE_ROWS["VIDEO"]]
        WHERE_ROW = YOUTUBE_ROWS["USER"]

        class Name(Methods):
            TABLE = YOUTUBE_TABLE
            SELECT_ROW = YOUTUBE_ROWS["CHANNEL_NAME"]
            WHERE_ROW = YOUTUBE_ROWS["USER"]

            @classmethod
            async def update(cls, channel_name: str, channel_name_old: str, user_id: str | int):
                await Database.sql_update(cls.TABLE, cls.SELECT_ROW, channel_name, cls.WHERE_ROW, str(user_id),
                                          channel_name=channel_name_old)

            @classmethod
            async def delete(cls, channel_name: str, user_id: str | int):
                await Database().sql_delete(cls.TABLE, cls.WHERE_ROW, str(user_id),
                                            channel_name=channel_name)

        class Url(Methods):
            TABLE = YOUTUBE_TABLE
            SELECT_ROW = YOUTUBE_ROWS["URL"]
            WHERE_ROW = YOUTUBE_ROWS["USER"]

            @classmethod
            async def delete(cls, channel_url: str, user_id: str | int):
                await Database().sql_delete(cls.TABLE, cls.WHERE_ROW, str(user_id),
                                            channel_url=channel_url)

        class VideoId:
            TABLE = YOUTUBE_TABLE
            SELECT_ROW = YOUTUBE_ROWS["VIDEO"]
            WHERE_ROW = YOUTUBE_ROWS["USER"]

            @classmethod
            async def update(cls, video_id: str, video_id_old: str, user_id: str | int):
                await Database.sql_update(cls.TABLE, cls.SELECT_ROW, video_id, cls.WHERE_ROW, str(user_id),
                                          current_video=video_id_old)


if __name__ == "__main__":
    cur, base = sql_start()
