import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN, ADMIN_IDS
from utils import get_localized_text, LANGUAGES, set_user_lang, get_user_lang, is_command, save_user_message, broadcast_message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    lang = State()

@dp.message_handler(commands=["start", "lang"])
async def send_welcome(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    for code, lang in LANGUAGES.items():
        kb.insert(InlineKeyboardButton(lang, callback_data=f"lang_{code}"))
    await message.answer("Tilni tanlang / Choose language:", reply_markup=kb)

@dp.message_handler(commands=["lang"])
async def choose_language(message: types.Message):
    buttons = [
        [types.InlineKeyboardButton(text=name, callback_data=f"lang:{code}")]
        for code, name in LANGUAGES.items()
    ]
    await message.reply("Tilni tanlang:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))

@dp.callback_query_handler(lambda c: c.data.startswith("lang:"))
async def set_language(callback_query: types.CallbackQuery):
    lang_code = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id
    set_user_lang(user_id, lang_code)
    await callback_query.message.edit_text(get_localized_text("language_set", lang_code))
    save_user_message(message, lang, bot)

@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Siz admin emassiz.")
    await message.reply("Admin panel: /broadcast [xabar matni]")

@dp.message_handler(commands=["broadcast"])
async def broadcast(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Ruxsat yo‘q.")
    msg = message.text.split(" ", 1)
    if len(msg) < 2:
        return await message.reply("Xabar matnini kiriting.")
    await broadcast_message(bot, msg[1])
    await message.reply("Xabar barcha foydalanuvchilarga yuborildi.")

    if __name__ == "__main__":
    from aiogram import executor
    print("Bot ishlayapti...")
    executor.start_polling(dp, skip_updates=True)
