from loader import dp
from aiogram import executor
from aiogram.types import BotCommand
from src.handlers import main
from src.handlers.user import emigrant 
from src.handlers.special import specialist, payment



async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("start", "restart bot")
    ])


executor.start_polling(dp, skip_updates=False, on_startup=set_default_commands)