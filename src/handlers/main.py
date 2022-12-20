from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from loader import dp, html, bot, db
from src.keyboards.reply import status_markup
from src.keyboards.inline import profile_markup, countries_markup, tariffs_markup
from config import PAYMENT_TOKEN

@dp.message_handler(CommandStart(), state="*")
async def start_command(msg: Message, state: FSMContext):
    await state.finish()
    user=db.get_user(msg.chat.id)
    if not(user):
        await msg.answer("Привет, приветственное сообщение ", reply_markup=status_markup)
    if user[3] == 'emigrant':
        await msg.answer("Привет, приветственное сообщение ", reply_markup=status_markup)
    else:
        await msg.answer("Привет, приветственное сообщение для специалиста", reply_markup=profile_markup)

@dp.message_handler(commands=['t'], state="*")
async def start_command(msg: Message, state: FSMContext):
    await bot.send_invoice(
            chat_id= msg.chat.id,
            title="Подписка на 1 месяц",
            description="Подписка дающая статус Специалиста на 1 месяц",
            provider_token=PAYMENT_TOKEN,
            currency="rub",
            prices=[LabeledPrice(label="1 месяц", amount=10000)],
            payload="0"
        )
    
    
@dp.callback_query_handler(text_contains='prof_')
async def prof_handler(call: CallbackQuery):
    if call.data.split('_')[1] == 'reg':
        await call.message.edit_text("Выберите страны:", reply_markup=countries_markup([]))
    else:
        await call.message.edit_text("Выберите желаемый тариф:", reply_markup=tariffs_markup)


@dp.message_handler(Text(equals=['Мой профиль']))
async def profile_handler(msg: Message):
    user= db.get_specialist(msg.chat.id)
    await msg.answer(f"""
ID: {user[0]}
Имя: {user[2]} {user[3]}
Username: {user[1]}
Страны: {user[4]}
Регионы: {user[5]}
Специальность {user[6]}
Контакты: {user[7]}
Подписка:
Дата окончания подписки:
                     """,
                     reply_markup=profile_markup,
                     parse_mode=html)