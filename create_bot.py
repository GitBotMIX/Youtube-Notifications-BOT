import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import I18N_DOMAIN, LOCALES_DIR, TOKEN
from aiogram.contrib.middlewares.i18n import I18nMiddleware

storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n)

_ = i18n.gettext
