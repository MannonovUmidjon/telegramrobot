from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

BOT_TOKEN = "YOUR_BOT_TOKEN"

# FUNKSIYALARGA TEGILMADI
def start(update, context):
    update.message.reply_text("Botga xush kelibsiz!")

def help_command(update, context):
    update.message.reply_text("Yordam uchun bu yerda man.")

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Qo‘shilgan handlerlar (aslidagi funksiyalar)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Botni ishga tushurish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
