from django.core.management.base import BaseCommand
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
from db import get_db_handle as db

data = json.load(open('telebot.json'))

TOKEN = data['token']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton(text="Поделиться номером телефона", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Нажмите на копку \"Поделиться номером телефона\"",
        reply_markup=reply_markup
    )

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        col = db()['telebot']
        query = {'phone': contact.phone_number}
        doc = col.find_one(query)
        if doc:
            pass
        else:
            x = col.insert_one({'phone': contact.phone_number, 'chatid': contact.user_id})
        await update.message.reply_text(f"Спасибо! Теперь код подтверждения будет отправляться сюда.")
    else:
        pass

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **kwargs):
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

        self.stdout.write(self.style.SUCCESS("Bot is running..."))
        app.run_polling()