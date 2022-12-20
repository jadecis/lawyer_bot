from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, PollAnswer
from loader import dp, html, bot, Spec, db
from src.keyboards.inline import accept_markup, tariffs_markup, countries_markup, special_markup
from src.keyboards.inline import contact_markup, usa_regions_markup
from src.keyboards.reply import specProfle_markup

@dp.message_handler(Text(equals=['Я специалист']))
async def iem_handler(msg: Message, state: FSMContext):
    try: 
        db.add_user(
            user_id=msg.chat.id,
            user_name=msg.chat.username,
            status='specialist'
        )
    except:
        
        db.update_user(
            user_id=msg.chat.id,
            user_name=msg.chat.username,
            status='specialist'
        )  
    finally:
        await msg.answer("Краткое описание функционала c условиями", reply_markup=accept_markup)
        
@dp.callback_query_handler(text_contains= 'accept_')
async def accept_handler(call: CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == "True":
        await call.message.edit_text("Выберите желаемый тариф:", reply_markup=tariffs_markup)
    else:
        await call.message.answer("Для работы в нашем боте вы должны принять наши условия!")
        
@dp.callback_query_handler(text_contains= 'tar_')
async def tar_handler(call: CallbackQuery, state: FSMContext):
    price= call.data.split('_')[1]
    await call.message.answer("Выберите страны:", reply_markup=countries_markup([]))
    
@dp.callback_query_handler(text_contains="cn_")
async def c_handler(call: CallbackQuery, state: FSMContext):
    data= await state.get_data()
    if call.data.split('_')[1] == 'accept':
        if data.get('arr_c').__contains__('USA'):
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup([], start_i=0, stop_i=10))
        else:
            await call.message.edit_text("Выберите специализацию:",reply_markup= special_markup)
    else:
        arr= [] if not(data.get('arr_c')) else data.get('arr_c')
        arr.append(call.data.split('_')[1])
        await state.update_data(arr_c=arr)
        await call.message.edit_text("Выберите страны:", reply_markup=countries_markup(arr))
    
@dp.callback_query_handler(text_contains="chn_")
async def ch_handler(call: CallbackQuery, state: FSMContext):
    data= await state.get_data()
    arr= [] if not(data.get('arr_c')) else data.get('arr_c')
    arr.remove(call.data.split('_')[1])
    await state.update_data(arr_c=arr)
    await call.message.edit_text("Выберите страны:", reply_markup=countries_markup(arr))
    
@dp.callback_query_handler(text_contains="reg_")
async def reg_handler(call: CallbackQuery, state: FSMContext):    
    response= call.data.split('_')
    data= await state.get_data()
    arr= [] if not(data.get('region')) else data.get('region')
    if response[1] == 'accept':
        str_arr= [str(i) for i in arr]
        await state.update_data(region=str_arr)
        await call.message.edit_text("Выберите специализацию:",reply_markup= special_markup)
    elif response[1] == 'next':
        if int(response[2]) > 49:
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=40, stop_i=50))
        else:
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=int(response[2]),
                                                                                          stop_i=int(response[2])+10))
    elif response[1] == 'ago':
        if int(response[2]) < 11:
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=0, stop_i=10))
        else:
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=int(response[2])-20,
                                                                                          stop_i=int(response[2])-10
                                                                                          ))
    elif response[1] == 'ch':
        arr.remove(int(response[2]))
        await state.update_data(region=arr)
        if int(response[3]) == 10:
             await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=0,
                                                                                          stop_i=10
                                                                                          ))
        else:
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=int(response[3])-10,
                                                                                          stop_i=int(response[3])
                                                                                          ))
    else:
        arr.append(int(response[1]))
        await state.update_data(region=arr)
        if int(response[2]) == 10:
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=0,
                                                                                          stop_i=10
                                                                                          ))
        else:
            await call.message.edit_text("Выберите регионы:", reply_markup=usa_regions_markup(arr, start_i=int(response[2])-10,
                                                                                          stop_i=int(response[2])
                                                                                          ))
        
@dp.callback_query_handler(text_contains='spec_')
async def spec_handler(call: CallbackQuery, state: FSMContext):
    special=call.data.split('_')[1]
    await state.update_data(spec= special)
    if call.message.chat.username:
        await call.message.edit_text("Выберите способ связи с вами:", reply_markup=contact_markup)
    else:
        await call.message.edit_text("Напишите номер телефона для связи с вами:")     
        await Spec.number.set()   
    
@dp.callback_query_handler(text_contains='cont_')
async def spec_handler(call: CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == 'number':
        await call.message.edit_text("Напишите номер телефона для связи с вами:")     
        await Spec.number.set()  
    else:
        data= await state.get_data()
        region= ",".join(data.get('region')) if data.get('region') else None
        coun= ",".join(data.get('arr_c')) if data.get('arr_c') else None
        emigr_name= call.message.chat.first_name if call.message.chat.first_name else ""
        emigr_name+= f" {call.message.chat.last_name}" if call.message.chat.last_name else ""
        user={
            'user_id' : call.message.chat.id,
            'user_name' : call.message.chat.username,
            'first_name' : call.message.chat.first_name,
            'last_name' : call.message.chat.last_name,
            'country' : coun,
            'region' : region,
            'special' : int(data.get('spec')),
            'contact' : f"@{call.message.chat.username}"
            }
        try:
            db.add_specialist(
                user=user
            )    
        except Exception as ex:
            print(ex)
            db.update_specialist(
                user=user
            )
        temp= str(data.get('arr_c'))[1:-1].split(',')
        res= db.get_emigrants_by({
            'counrty' : ','.join(temp),
            'special' : int(data.get('spec'))
        })
        list_emigrant=""
        print(data.get('region'))
        if data.get('region'):
            for i in res:
                if data.get('region').__contains__(str(i[5])):
                    spec_name= i[2] if i[2] else ""
                    spec_name+=f" {i[3]}" if i[3] else ""
                    await bot.send_message(chat_id=i[0], text=
f"Добрый день, «{spec_name}», в наш бот зарегистрировался специалист «{emigr_name}»,"
+f"Он подходит вам для осуществления ваших запросов. Вы можете связаться с ним - @{call.message.chat.username}")
                    list_emigrant+=f"\n{spec_name}, связаться с ним @{i[1]}"
                res.remove(i)
        for i in res:
            spec_name= i[2] if i[2] else ""
            spec_name+=f" {i[3]}" if i[3] else ""
            list_emigrant+=f"\n{spec_name}, связаться с ним @{i[1]}"
            await bot.send_message(chat_id=i[0], text=
f"Добрый день, «{spec_name}», в наш бот зарегистрировался специалист «{emigr_name}»,"
+f"Он подходит вам для осуществления ваших запросов. Вы можете связаться с ним - @{call.message.chat.username}")
            
        await call.message.delete()
        await call.message.answer(f"""
Поздравляю вы прошли регистрацию!
Мы подобрали подходящих эмигрантов с похожими задачами. Вот список тех, к кому вы можете помочь:
{list_emigrant}""", reply_markup=specProfle_markup)
        await state.finish()
            
@dp.message_handler(content_types=['text'], state= Spec.number)
async def number_handler(msg: Message, state: FSMContext):
    data= await state.get_data()
    emigr_name= msg.chat.first_name if msg.chat.first_name else ""
    emigr_name+= f" {msg.chat.last_name}" if msg.chat.last_name else ""
    user={
        'user_id' : msg.chat.id,
        'user_name' : msg.chat.username,
        'first_name' : msg.chat.first_name,
        'last_name' : msg.chat.last_name,
        'country' : ",".join(data.get('arr_c')),
        'region' : ",".join(data.get('region')),
        'special' : data.get('spec'),
        'contact' : msg.text
    }
    try:
        db.add_specialist(
            user=user
        )
        
    except:
        db.update_specialist(
            user=user
        )
    temp= str(data.get('arr_c'))[1:-1].split(',')
    res= db.get_emigrants_by({
        'counrty' : ','.join(temp),
        'special' : int(data.get('spec'))
    })
    print(res)
    list_emigrant=""
    if data.get('region'):
        for i in res:
            if data.get('region').__contains__(str(i[5])):
                print(123)
                spec_name= i[2] if i[2] else ""
                spec_name+=f" {i[3]}" if i[3] else ""
                await bot.send_message(chat_id=i[0], text=
f"Добрый день, «{spec_name}», в наш бот зарегистрировался специалист «{emigr_name}»,"
+f"Он подходит вам для осуществления ваших запросов. Вы можете связаться с ним - @{msg.text}")
                list_emigrant+=f"\n{spec_name}, связаться с ним @{i[1]}"
            res.remove(i)
    for i in res:
        spec_name= i[2] if i[2] else ""
        spec_name+=f" {i[3]}" if i[3] else ""
        list_emigrant+=f"\n{spec_name}, связаться с ним @{i[1]}"
        await bot.send_message(chat_id=i[0], text=
f"Добрый день, «{spec_name}», в наш бот зарегистрировался специалист «{emigr_name}»,"
+f"Он подходит вам для осуществления ваших запросов. Вы можете связаться с ним - @{msg.text}")
        
    
    await msg.answer(f"""
Поздравляю вы прошли регистрацию!
Мы подобрали подходящих эмигрантов с похожими задачами. Вот список тех, к кому вы можете помочь:
{list_emigrant}""", reply_markup=specProfle_markup)
    await state.finish()
    
    
