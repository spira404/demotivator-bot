from aiogram import Dispatcher, types, Bot, F
from aiogram.filters import Command

import asyncio
import time
import logging

from os import getenv
from dotenv import load_dotenv

from draw_demotivator import make_dem

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()

logging.basicConfig(filename=".main.log",
        level=logging.WARNING, 
        filemode="a",
        format="%(asctime)s %(levelname)s %(module)s - %(funcName)s \n%(message)s\n|\n|\n|", 
        datefmt="%d/%m/%Y %I:%M:%S %p"
        )

@dp.message(Command("start"))
async def greet(mes: types.Message):
    await bot.send_message(mes.from_user.id,
        f"""\
Отправь картинку с текстом - получи демотиватор. Две строки - не больше.
""",
        parse_mode="HTML") 

@dp.message()
async def draw_dem(mes: types.Message):
    try:
        photo = mes.photo[-1]
        file = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file.file_path)
        if mes.caption:
            demotivator = make_dem(photo_bytes.getvalue(), mes.caption)
        else:
            demotivator = make_dem(photo_bytes.getvalue(), "дурачина\nтекст не ввел")
        await bot.send_photo(mes.from_user.id, photo=types.input_file.BufferedInputFile(demotivator.getvalue(), filename="out.png"))
    except Exception as e:
        await bot.send_message(mes.from_user.id, "Неверный ввод")
        logging.warning(e)

async def main():
    await dp.start_polling(
        bot, 
        skip_updates=True,
        handle_signals=False)

if __name__ == "__main__":
    asyncio.run(main())

