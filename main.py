from flask import Flask, request
import telebot

API_TOKEN = 'YOUR_BOT_TOKEN'  # ← bu yerga tokeningizni yozing
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# Webhook qabul qiluvchi marshrut
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

# Test sahifa (majburiy emas, faqat tekshirish uchun)
@app.route('/')
def index():
    return "Bot ishlayapti!"

if __name__ == "__main__":
    app.run()
