from aiogram import types
from datetime import datetime
from collections import defaultdict

LANGUAGES = {
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
    "en": "🇺🇸 English",
    "tr": "🇹🇷 Türkçe",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "it": "🇮🇹 Italiano",
    "es": "🇪🇸 Español",
    "zh": "🇨🇳 中文",
    "ar": "🇸🇦 العربية"
}

texts = {
    "language_set": {
        "uz": "Til tanlandi.",
        "ru": "Язык выбран.",
        "en": "Language set.",
        "tr": "Dil ayarlandı.",
        "de": "Sprache eingestellt.",
        "fr": "Langue définie.",
        "it": "Lingua impostata.",
        "es": "Idioma establecido.",
        "zh": "语言设置成功。",
        "ar": "تم تعيين اللغة."
    },
    "message_sent": {
        "uz": "Xabaringiz yuborildi.",
        "ru": "Ваше сообщение отправлено.",
        "en": "Your message has been sent.",
        "tr": "Mesajınız gönderildi.",
        "de": "Ihre Nachricht wurde gesendet.",
        "fr": "Votre message a été envoyé.",
        "it": "Il tuo messaggio è stato inviato.",
        "es": "Tu mensaje ha sido enviado.",
        "zh": "您的消息已发送。",
        "ar": "تم إرسال رسالتك."
    }
}

user_langs = defaultdict(lambda: "uz")

def get_localized_text(key, lang):
    return texts.get(key, {}).get(lang, texts[key]["en"])

def set_user_lang(user_id, lang):
    user_langs[user_id] = lang

def get_user_lang(user_id):
    return user_langs[user_id]

def is_command(text):
    return text.startswith("/")

async def save_user_message(message: types.Message, lang: str, bot):
    info = (
        f"🆔 {message.from_user.id}
"
        f"👤 @{message.from_user.username}
"
        f"🗣 {message.text}"
    )
    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, info)

async def broadcast_message(bot, text):
    for user_id in user_langs:
        try:
            await bot.send_message(user_id, text)
        except:
            continue
