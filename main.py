import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import BOT_TOKEN, ADMIN_IDS
from utils import get_localized_text, LANGUAGES, set_user_lang, get_user_lang, is_command, save_user_message, broadcast_message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# START yoki LANG
@dp.message_handler(commands=["start", "lang"])
async def send_welcome(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    for code, lang in LANGUAGES.items():
        kb.insert(InlineKeyboardButton(lang, callback_data=f"lang:{code}"))
    await message.answer("Tilni tanlang / Choose language:", reply_markup=kb)

# TIL TANLASH CALLBACK
@dp.callback_query_handler(lambda c: c.data.startswith("lang:"))
async def set_language(callback_query: types.CallbackQuery):
    lang_code = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id
    set_user_lang(user_id, lang_code)
    await callback_query.message.edit_text(get_localized_text("language_set", lang_code))
    await callback_query.answer()
    await bot.send_message(user_id, get_localized_text("message_sent", lang_code))

# ADMIN PANEL
@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Siz admin emassiz.")
    await message.reply("Admin panel: /broadcast [xabar matni]")

# ADMIN BROADCAST
@dp.message_handler(commands=["broadcast"])
async def broadcast(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Ruxsat yo‘q.")
    msg = message.text.split(" ", 1)
    if len(msg) < 2:
        return await message.reply("Xabar matnini kiriting.")
    await broadcast_message(bot, msg[1])
    await message.reply("Xabar barcha foydalanuvchilarga yuborildi.")

# FOYDALANUVCHIDAN ODDIY XABAR
@dp.message_handler(lambda message: not is_command(message.text))
async def handle_user_message(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await save_user_message(message, lang, bot)
    await message.reply(get_localized_text("message_sent", lang))

# BOTNI ISHGA TUSHURISH
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
