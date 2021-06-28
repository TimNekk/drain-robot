from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class IsLink(BoundFilter):
    async def check(self, message: Message) -> bool:
        return 'vk.com/' in message.text or 'instagram.com/' in message.text or 'tiktok.com/' in message.text
