import hashlib
from asyncio import sleep
from datetime import datetime
from random import randint, choice
from string import ascii_letters

from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.exceptions import BadRequest
from aiogram.utils.markdown import hlink

from filters import IsLink, IsInDB
from keyboards.inline import buy_keyboard
from loader import dp, db
from utils.db_api.classes.link import WrongUrlError


@dp.message_handler(IsInDB(), IsLink())
async def bot_echo(message: types.Message):
    link = 'http://' + message.text if 'http://' in message.text else message.text
    try:
        link = db.get_link(link)
    except WrongUrlError:
        await message.answer('<b>Что-то не так с ссылкой</b>\n\nМожно отправлюять ссылки на профиль в <b>VK</b>, <b>Instagram</b>, <b>TikTok</b>')
        return

    message = await message.answer('<b>👤 Анализ ссылки пользователя...</b>')
    await sleep(randint(50, 200) / 100)
    await message.delete()

    text = link.user_text
    with open('photo.jpg', 'wb') as f:
        f.write(link.user['image'])
    try:
        message = await message.answer_photo(InputFile('photo.jpg'), text)
    except BadRequest:
        message = await message.answer_photo(InputFile('avatar.jpg'), text)

    for place in link.places:
        time = randint(*(place[2]))
        text += f"🔍<b> {place[0]}</b> (≈ {place[1]})\n"
        await message.edit_caption(text)
        await sleep(time)
        text += f"{'✅' if place[3] else '❌'} Найдено файлов: <b>{place[3]}</b>\n\n"

    for n in range(link.total_count):
        new_text = text + f'<b>⚙️ Подготовка и структуризация файлов {n}/{link.total_count}...</b>'
        message = await message.edit_caption(new_text)
        # await sleep(randint(30, 100) / 100)

    await message.edit_caption('\n'.join(link.text), reply_markup=buy_keyboard(link.total_count, link.price_with_discount))
