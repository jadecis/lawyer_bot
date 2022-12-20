from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from loader import dp, html, bot, User, db
from src.keyboards.inline import country_markup, special_markup, user_region


@dp.message_handler(Text(equals=['Я эмигрант']), state="*")
async def iem_handler(msg: Message, state: FSMContext):
    await state.finish()
    try: 
        db.add_user(
            user_id=msg.chat.id,
            user_name=msg.chat.username,
            status='emigrant'
        )
    except:
        db.update_user(
            user_id=msg.chat.id,
            user_name=msg.chat.username,
            status='emigrant'
        )
        
    finally:
        await msg.answer("Краткое описание функционала\n\nВыберите страну: ", reply_markup=country_markup)
        await User.region.set()
    
@dp.callback_query_handler(text_contains='country_', state=User.region)
async def country_handler(call: CallbackQuery, state: FSMContext):
    place=call.data.split('_')[1]
    await state.update_data(user_country=place)
    if place == 'USA':
        await call.message.edit_text("Выберите регион:", reply_markup=user_region(start_i=0, stop_i=10))
    else:
        await call.message.edit_text("Выберите специализацию", reply_markup=special_markup)


@dp.callback_query_handler(text_contains="reg_", state=User.region)
async def reg_handler(call: CallbackQuery, state: FSMContext):
    response= call.data.split('_')
    if response[1] == 'next':
        if int(response[2]) > 49:
            await call.message.edit_text("Выберите регион:", reply_markup=user_region(start_i=40, stop_i=50))
        else:
            await call.message.edit_text("Выберите регион:", reply_markup=user_region(start_i=int(response[2]),
                                                                                          stop_i=int(response[2])+10))
    elif response[1] == 'ago':
        if int(response[2]) < 11:
            await call.message.edit_text("Выберите регион:", reply_markup=user_region(start_i=0, stop_i=10))
        else:
            await call.message.edit_text("Выберите регион:", reply_markup=user_region(start_i=int(response[2])-20,
                                                                                          stop_i=int(response[2])-10
                                                                                          ))
    else:
        await state.update_data(region_user=str(response[1]))
        await call.message.edit_text("Выберите специализацию", reply_markup=special_markup)
    
@dp.callback_query_handler(text_contains="spec_", state=User.region)
async def special_handler(call: CallbackQuery, state: FSMContext):
    special=call.data.split('_')[1]
    await state.update_data(user_spec= special)
    await call.message.answer("Кратко опишите ситуацию:\n\nНебольше 300 символов!")
    await User.situation.set()
    
@dp.message_handler(content_types=['text'], state=User.situation)
async def situation_handler(msg: Message, state=FSMContext):
    emigr_name= msg.chat.first_name if msg.chat.first_name else ""
    emigr_name+= f" {msg.chat.last_name}" if msg.chat.last_name else ""
    if len(msg.text) <= 300:
        data = await state.get_data()
        user= {
                "user_id" : msg.chat.id,
                "user_name" : msg.from_user.username,
                "first_name": msg.from_user.first_name,
                "last_name" : msg.from_user.last_name,
                "country" : data.get("user_country"),
                "region" : data.get("region_user"),
                "special" : data.get("user_spec"),
                "problem" : msg.text
                }
        try:
            db.add_emigrant(
                user=user
            )
        except Exception as ex: 
            print(ex)
            db.update_emigrant(
                user=user
            )
        res= db.get_specialists_by(special=int(data.get("user_spec")))
        list_special=""
        for i in res:
            if data.get("region_user"):
                if i[5].split(',').__contains__(data.get("region_user")):
                    spec_name= i[2] if i[2] else ""
                    spec_name+=f" {i[3]}" if i[3] else ""
                    await bot.send_message(chat_id=i[0], text=
f"Добрый день, «{spec_name}», нашему боту поступила заявка от эмигранта «{emigr_name}»,"
+f"вы подходите для осуществления его запросов. Вы можете связаться с ним - @{msg.chat.username}")
                    list_special+=f'\n{spec_name}, связаться с ним {i[7]}'
                else:
                    res.remove(i)
            else:
                if i[4].split(',').__contains__(data.get("user_country")):
                    spec_name= i[2] if i[2] else ""
                    spec_name+=f" {i[3]}" if i[3] else ""
                    await bot.send_message(chat_id=i[0], text=
f"Добрый день, «{spec_name}», нашему боту поступила заявка от эмигранта «{emigr_name}»,"
+f"вы подходите для осуществления его запросов. Вы можете связаться с ним - @{msg.chat.username}")
                    list_special+=f'\n{spec_name}, связаться с ним {i[7]}'
                else:
                    res.remove(i)
        if list_special:
            await msg.answer(f"""
Поздравляю вы прошли регистрацию!
Мы подобрали подходящих специалистов для осуществления ваших задач. Вот список тех, к кому вы можете обратиться:
{list_special}""")
        else:
            await msg.answer(f"""Поздравляю вы прошли регистрацию!""")
        await state.finish()
    else:
        await msg.answer("Превышен лимит символов! Опишите еще раз ситуацию!\n\nНебольше 300 символов!")