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

@dp.callback_query_handler(Text(startswith="lang_"))
async def set_language(call: types.CallbackQuery):
    lang_code = call.data.split("_")[1]
    set_user_lang(call.from_user.id, lang_code)
    await call.message.edit_text(get_localized_text("language_set", lang_code))

@dp.message_handler(lambda message: not is_command(message.text))
async def handle_message(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    text = get_localized_text("message_sent", lang)
    await message.answer(text)
    save_user_message(message, lang, bot)

@dp.message_handler(commands=["admin"], user_id=ADMIN_IDS)
async def admin_panel(message: types.Message):
    await message.answer("Admin panel: yuboriladigan xabarni kiriting yoki buyruq tanlang.")

@dp.message_handler(commands=["broadcast"], user_id=ADMIN_IDS)
async def broadcast_cmd(message: types.Message):
    text = message.get_args()
    await broadcast_message(bot, text)
    await message.answer("Xabar yuborildi.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
