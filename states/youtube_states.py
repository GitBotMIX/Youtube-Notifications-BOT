from aiogram.dispatcher.filters.state import State, StatesGroup


class AddChannel(StatesGroup):
    channel_name = State()
    channel_url = State()
    channel_video_url = State()