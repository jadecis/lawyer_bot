from aiogram.types import ReplyKeyboardMarkup

status_markup= ReplyKeyboardMarkup(resize_keyboard=True)

status_markup.add(
    'Я специалист', 
    'Я эмигрант'
)

specProfle_markup= ReplyKeyboardMarkup(resize_keyboard=True)

specProfle_markup.add(
    'Мой профиль'
)