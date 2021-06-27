import logging
import os

from aiogram import executor

from data.config import log_folder
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

handlers
filters
middlewares


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    # Create Log folder
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    # Logging
    logging.info('Bot started')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
