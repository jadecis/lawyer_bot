from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.database.other import list_region_usa

special_markup=InlineKeyboardMarkup(row_width=2)

special_markup.add(
    InlineKeyboardButton('Юридические услуги', callback_data="spec_0"),
    InlineKeyboardButton('Банковские услуги', callback_data="spec_1"),
    InlineKeyboardButton('Дети и образование', callback_data="spec_2"),
    InlineKeyboardButton('Здравоохранение', callback_data="spec_3"),
    InlineKeyboardButton('Изучение языков', callback_data="spec_4"),
    InlineKeyboardButton('Недвижимость', callback_data="spec_5"),
    InlineKeyboardButton('Политическое убежище', callback_data="spec_6"),
    InlineKeyboardButton('Поручительство', callback_data="spec_7"),
    InlineKeyboardButton('Транспорт', callback_data="spec_8"),
    InlineKeyboardButton('Услуги переводчика', callback_data="spec_9")
)

country_markup= InlineKeyboardMarkup(row_width=2)

country_markup.add(
    InlineKeyboardButton("США", callback_data="country_USA"),
    InlineKeyboardButton("ОАЭ", callback_data="country_UAE"),
    InlineKeyboardButton("Россия", callback_data="country_RUS"),
    InlineKeyboardButton("Турция", callback_data="country_TUR")
)
def user_region(start_i, stop_i):
    markup= InlineKeyboardMarkup(row_width=3)
    for i in range(start_i, stop_i):
        for k, v  in list_region_usa[i].items():
            markup.insert(
                InlineKeyboardButton(f"{k}", callback_data=f"reg_{v}")
                )
    markup.add(
        InlineKeyboardButton(f"⬅️", callback_data=f"reg_ago_{stop_i}"),
        InlineKeyboardButton(f"➡️", callback_data=f"reg_next_{stop_i}")
    )
    return markup
            



accept_markup= InlineKeyboardMarkup(row_width=1)

accept_markup.add(
    InlineKeyboardButton("✅ Принять", callback_data="accept_True"),
    InlineKeyboardButton("❌ Отклонить", callback_data="accept_False")
)

tariffs_markup= InlineKeyboardMarkup(row_width=1)

tariffs_markup.add(
    InlineKeyboardButton('1 мес - 35$', callback_data="tar_35"),
    InlineKeyboardButton('3 мес - 90$', callback_data="tar_90"),
    InlineKeyboardButton('6 мес - 180$', callback_data="tar_180"),
    InlineKeyboardButton('12 мес - 350$', callback_data="tar_350"),
)

contact_markup= InlineKeyboardMarkup(row_width=1)

contact_markup.add(
    InlineKeyboardButton('По телефону', callback_data="cont_number"),
    InlineKeyboardButton('Сообщение в лс телеграмма', callback_data="cont_lm"),
)

def countries_markup(list_country: list):
    markup= InlineKeyboardMarkup(row_width=2)
    country= {
        'США' : 'USA',
        'ОАЭ' : 'UAE',
        'Россия' : 'RUS',
        'Турция' : 'TUR'
    }
    for k, v in country.items():
        if list_country.__contains__(v):
            markup.insert(
                InlineKeyboardButton(f"☑️ {k}", callback_data=f"chn_{v}")
                )
        else:
            markup.insert(
                InlineKeyboardButton(f"{k}", callback_data=f"cn_{v}")
                )
    markup.add(InlineKeyboardButton(f"✅ Подтвердить выбор", callback_data=f"cn_accept"))
    
    return markup

profile_markup= InlineKeyboardMarkup(row_width=1)

profile_markup.add(
    InlineKeyboardButton('Пройти регистрацию заново', callback_data="prof_reg"),
    InlineKeyboardButton('Продлить подписку', callback_data="prof_sub"),
)

def usa_regions_markup(select_regions: list, start_i, stop_i):
    markup= InlineKeyboardMarkup(row_width=3)
    for i in range(start_i, stop_i):
        for k, v  in list_region_usa[i].items():
            if select_regions.__contains__(v):
                markup.insert(
                    InlineKeyboardButton(f"☑️ {k}", callback_data=f"reg_ch_{v}_{stop_i}")
                    )
            else:
                markup.insert(
                    InlineKeyboardButton(f"{k}", callback_data=f"reg_{v}_{stop_i}")
                    )
    markup.add(
        InlineKeyboardButton(f"⬅️", callback_data=f"reg_ago_{stop_i}"),
        InlineKeyboardButton(f"➡️", callback_data=f"reg_next_{stop_i}")
    )
    markup.add(
        InlineKeyboardButton(f"✅ Подтвердить выбор", callback_data=f"reg_accept")
        )
    return markup