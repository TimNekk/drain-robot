from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile

from filters import IsInDB
from loader import dp, db


@dp.message_handler(IsInDB(reverse=True), CommandStart())
async def bot_start_new(message: types.Message):
    db.add_user(message.chat.id)
    await bot_start(message)


@dp.message_handler(IsInDB(), CommandStart())
async def bot_start(message: types.Message):
    user = db.get_user(message.chat.id)

    text = [
        'Для получения сливов отправьте ссылку профиль в <b>VK</b>, <b>Instagram</b>, <b>TikTok</b>']
    await message.answer('\n'.join(text))