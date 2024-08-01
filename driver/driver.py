import time
import os
from pyvirtualdisplay import Display
import json
import threading
from db import get_db_handle as db
import subprocess


display = Display(visible=0, size=(1280, 768))
display.start()
print('display start')
env = os.environ.copy()
env['DISPLAY'] = display.new_display_var

import pyautogui

x = subprocess.Popen(['whatsapp-for-linux'], env=env)


"""
while True:
    x, y = pyautogui.position()
    positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    print(positionStr, end='')
    print('\b' * len(positionStr), end='', flush=True)
"""
def check_message():
    while True:
        col = db()['whatsapp']
        doc = col.find_one()
        if not doc == None:
            col.delete_one(doc)

            pyautogui.moveTo(68, 28)
            time.sleep(1)
            pyautogui.click()

            pyautogui.moveTo(496, 419)
            time.sleep(1)
            pyautogui.click()

            pyautogui.write(doc['phone'])
            pyautogui.press('enter')
            time.sleep(5)

            pyautogui.moveTo(746, 739)
            time.sleep(1)
            pyautogui.click()

            pyautogui.write(str(doc['code'])+' - Korshiles.kz')
            pyautogui.press('enter')
            time.sleep(5)
            pyautogui.press('escape')

        
        time.sleep(5)
        print('check message while')

periodic_thread = threading.Thread(target=check_message)
periodic_thread.start()

import telebot

data = json.load(open('driver/telebot.json'))
API_TOKEN = data['token']
CHAT_ID = data['chatid']
PHOTO_PATH = 'image.png'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('I have registered, what to do next?')
    markup.add(btn1)
    bot.send_message(message.from_user.id, 'hello', reply_markup=markup)


@bot.message_handler(commands=['sendphoto'])
def send_photo(message):
    im = pyautogui.screenshot(PHOTO_PATH)
    bot.send_photo(CHAT_ID, photo=open(PHOTO_PATH, 'rb'))


bot.infinity_polling()