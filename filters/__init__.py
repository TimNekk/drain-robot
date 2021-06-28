from aiogram import Dispatcher

from loader import dp
from .vk import IsLink
from .db import IsInDB


if __name__ == "filters":
    dp.filters_factory.bind(IsLink)
    dp.filters_factory.bind(IsInDB)
