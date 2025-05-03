from django.core.management.base import BaseCommand
import telebot
import os
import json
from db import get_db_handle as db


data = json.load(open('telebot.json'))
TOKEN = data['token']
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton("Поделиться номером телефона", request_contact=True)
    markup.add(button)
    bot.send_message(message.chat.id, "Нажмите на копку \"Поделиться номером телефона\"", reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact = message.contact
    if contact:
        col = db()['telebot']
        query = {'phone': contact.phone_number}
        doc = col.find_one(query)
        if doc:
            pass
        else:
            x = col.insert_one({'phone': contact.phone_number, 'chatid': contact.user_id})
        bot.send_message(message.chat.id, f"Спасибо! Теперь код подтверждения будет отправляться сюда.")
    else:
        pass


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        print("Bot is polling...")
        bot.infinity_polling()