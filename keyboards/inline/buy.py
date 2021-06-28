from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def buy_keyboard(files: int, price: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(f'Купить {files} файлов за {price}₽',
                                     callback_data=f'buy:{price}')
            ]
        ]
    )
    return keyboard


def paid_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='✅ Оплатил ✅',
                                         callback_data='paid'))

    keyboard.add(InlineKeyboardButton(text='🚫 Отмена 🚫',
                                         callback_data='cancel'))

    return keyboard
