

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class IsInDB(BoundFilter):
    key = 'reverse'

    def __init__(self, reverse=False):
        self.reverse = reverse

    async def check(self, message: types.Message):
        user = db.get_user(id=message.chat.id)
        return True if user and not self.reverse else \
            True if not user and self.reverse else False