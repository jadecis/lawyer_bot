from aiogram.types import LabeledPrice, Message, PreCheckoutQuery, ContentType, CallbackQuery
from aiogram.dispatcher import FSMContext
from loader import bot, dp, db 
from config import PAYMENT_TOKEN
from src.keyboards.inline import countries_markup

@dp.callback_query_handler(text_contains= 'tar_')
async def tar_handler(call: CallbackQuery, state: FSMContext):
    price= int(call.data.split('_')[1])
    if price== 35:
        await bot.send_invoice(
            call.message.chat.id,
            title="Подписка на 1 месяц",
            description="Подписка дающая статус Специалиста на 1 месяц",
            provider_token=PAYMENT_TOKEN,
            currency="rub",
            need_email=False,
            prices=[LabeledPrice(label="1 месяц", amount=3500)],
            start_parameter="example",
            payload='some_invoice'
        )
    if price== 90:
        await bot.send_invoice(
        call.message.chat.id,
        title="Подписка на 3 месяца",
        description="Подписка дающая статус Специалиста на 3 месяца",
        provider_token=PAYMENT_TOKEN,
        currency="rub",
        need_email=False,
        prices=[LabeledPrice(label="3 месяца", amount=9000)],
        start_parameter="example",
        payload='some_invoice'
    )
    if price== 180:
        await bot.send_invoice(
            call.message.chat.id,
            title="Подписка на 6 месяцев",
            description="Подписка дающая статус Специалиста на 6 месяцев",
            provider_token=PAYMENT_TOKEN,
            currency="USD",
            need_email=False,
            prices=[LabeledPrice(label="6 месяцев", amount=18000)],
            start_parameter="example",
            payload='some_invoice'
        )
    if price== 350:
        await bot.send_invoice(
            call.message.chat.id,
            title="Подписка на 12 месяцев",
            description="Подписка дающая статус Специалиста на 12 месяцев",
            provider_token=PAYMENT_TOKEN,
            currency="USD",
            need_email=False,
            prices=[LabeledPrice(label="12 месяцев", amount=35000)],
            start_parameter="example",
            payload='test'
        )
            


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre.id, ok=True)
    
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state="*")
async def succesful_payment(msg: Message):
    print(msg.successful_payment)
