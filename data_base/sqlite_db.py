import sqlite3 as sq


class Database:
    def __init__(self):
        self.base, self.cur = self.sql_start()

    def sql_start(self):
        base = sq.connect('Notifications.db')
        cur = base.cursor()
        if base:
            print('Data base connected OK!')
        base.execute('CREATE TABLE IF NOT EXISTS user(status TEXT, language TEXT, user_id TEXT)')
        base.execute('CREATE TABLE IF NOT EXISTS'
                     ' youtube(channel_name TEXT, channel_url TEXT, current_video TEXT, user_id TEXT)')
        base.commit()
        return base, cur


class Youtube(Database):
    YOUTUBE_TABLE = 'youtube'
    YOUTUBE_ROWS = {'CHANNEL_NAME': 'channel_name', 'URL': 'channel_url',
                    'VIDEO': 'current_video', 'USER': 'user_id'}

    def __init__(self):
        super().__init__()
        self.__table_data = None
        self.__table = None
        self.__row = None




    async def channel(self):
        async def from_user(user_id):
            pass

