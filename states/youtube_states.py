from aiogram.dispatcher.filters.state import State, StatesGroup


class AddChannel(StatesGroup):
    message = State()
    set_channel = State()