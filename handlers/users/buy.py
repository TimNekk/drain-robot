import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hlink

from keyboards.inline import paid_keyboard
from loader import dp, db
from utils.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.callback_query_handler(text_contains='buy')
async def bot_buy(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    amount = int(call.data.split(':')[1])

    payment = Payment(amount=amount)
    payment.create()

    await call.message.answer(
        text=hlink('Ссылка на оплату', url=payment.invoice),
        reply_markup=paid_keyboard()
    )

    await state.set_state('qiwi')
    await state.update_data(payment=payment,
                            amount=amount)


@dp.callback_query_handler(text='cancel', state='qiwi')
async def cancel_payment(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Отменено')
    await state.finish()


@dp.callback_query_handler(text='paid', state='qiwi')
async def approve_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get('payment')

    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer('Транзакция не найдена\nПо вопросам @TimNekk')
        return
    except NotEnoughMoney:
        await call.message.answer('Оплаченная сумма меньше необходимой'
                                  '\nПо вопросам @TimNekk')
        return
    else:
        user = db.get_user(id=call.message.chat.id)

        text = f"💸💸💸\n\n{await user.info} купил за {payment.amount}р\n{payment.id}\n\n💸💸💸"
        logging.info(text)

        user.add_paid(payment.amount)

        await call.message.answer('Купил!')

    await state.finish()


@dp.message_handler(state='qiwi')
async def notify_to_pay(message: Message, state: FSMContext):
    await message.answer(text='Для начала <i>оплатите</i> или <i>отмените</i> платеж')