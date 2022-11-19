import sqlite3 as sq
from constants import YOUTUBE_TABLE, YOUTUBE_ROWS, USER_TABLE, USER_ROWS


def sql_start():
    global cur, base
    base = sq.connect('Notifications.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS user(status TEXT, language TEXT, user_id TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS '
                 'youtube(channel_name TEXT, channel_url TEXT, current_video TEXT, user_id TEXT)')
    base.commit()
    return cur, base


class Database:
    @staticmethod
    async def sql_add(args: tuple, table_name):
        rows_value_str = '?, '
        cur.execute(f'INSERT INTO {table_name} VALUES ({(rows_value_str * len(args))[0:-2]})', args)
        base.commit()

    @staticmethod
    async def sql_delete(table_name: str, where: str, where_data: tuple, **and_data):
        if and_data:
            print('Сработала AND_DATA (27)')
            and_sql_str = [i[0] for i in and_data]
            and_data_list = [i[1] for i in and_data]
            and_sql_generated_str = ''
            for i in and_sql_str:
                and_sql_generated_str += f' AND {i} == ?'
            cur.execute(f'DELETE FROM {USER_TABLE} WHERE {USER_ROWS["USER"]} == ?{and_sql_generated_str}',
                        tuple(and_data_list))
            base.commit()
        cur.execute(f'DELETE FROM {table_name} WHERE {where} == ?', where_data)
        base.commit()


async def tuple_list_to_list_first_values_in_tuple(list_tuple: list[tuple]) -> list:
    list_values = [i[0] for i in list_tuple]
    return list_values


class User:
    @staticmethod
    async def add(*args: str):
        await Database().sql_add(args, USER_TABLE)

    @staticmethod
    async def delete(user_id: str):
        await Database().sql_delete(USER_TABLE, USER_ROWS['USER'], (user_id,))

    @staticmethod
    async def get_user(user_id):
        user_id_tuple_list = cur.execute(f'SELECT {USER_ROWS["USER"]} '
                                         f'FROM {USER_TABLE} '
                                         f'WHERE {USER_ROWS["USER"]} == ?', (str(user_id),)).fetchone()
        return user_id_tuple_list

    class Status:
        @staticmethod
        async def to_premium(user_id):
            user_id = str(user_id)
            cur.execute(f'UPDATE {USER_TABLE} SET {USER_ROWS["STATUS"]} == ? '
                        f'WHERE {USER_ROWS["USER"]} == ?', ('premium', user_id,))
            base.commit()

        @staticmethod
        async def where_user(user_id):
            status_tuple_list = cur.execute(f'SELECT {YOUTUBE_ROWS["URL"]} '
                                            f'FROM {YOUTUBE_TABLE} '
                                            f'WHERE {YOUTUBE_ROWS["USER"]} == ?', (user_id,)).fetchall()
            return status_tuple_list


class Youtube:
    @staticmethod
    async def add(*args: str):
        await Database().sql_add(args, YOUTUBE_TABLE)

    @staticmethod
    async def delete(user_id: str):
        await Database().sql_delete(USER_TABLE, USER_ROWS['USER'], (user_id,))

    class Channel:
        @staticmethod
        async def where_user(user_id):
            channels_tuple_list = cur.execute(f'SELECT {YOUTUBE_ROWS["URL"]} '
                                              f'FROM {YOUTUBE_TABLE} '
                                              f'WHERE {YOUTUBE_ROWS["USER"]} == ?', (user_id,)).fetchall()
            return channels_tuple_list

        @staticmethod
        async def get_all():
            channels_tuple_list = cur.execute(f'SELECT {YOUTUBE_ROWS["URL"]} '
                                              f'FROM {YOUTUBE_TABLE}').fetchall()
            return channels_tuple_list


if __name__ == "__main__":
    cur, base = sql_start()
