from selenium import webdriver
from chromedriver_py import binary_path
import time
import os
from pyvirtualdisplay import Display
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext
import asyncio
import json
import threading
from db import get_db_handle as db


display = Display(visible=1, size=(1920, 1080))
display.start()
print('display start')


options = webdriver.ChromeOptions()
data = os.getcwd() + '/driver/driver-data'
options.add_argument('--user-data-dir=' + data)


# Options
#options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-software-rasterizer')
options.add_argument("--disable-application-cache")
options.add_argument("--disable-in-process-stack-traces")
options.add_argument("--disable-logging")
options.add_argument("--disable-extensions")
options.add_argument("--disable-renderer-backgrounding")
#options.add_argument("--disable-background-networking")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-backgrounding-occluded-windows")
options.add_argument("--disable-breakpad")
options.add_argument("--disable-component-extensions-with-background-pages")
options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
options.add_argument("--disable-ipc-flooding-protection")
#options.add_argument("--single-process")
#options.add_argument('user-agent=User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
print('options setted')


service = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=service, options=options)
print('driver start')


driver.get('https://web.whatsapp.com/')


# Variables whatsapp
AUTH_BUTTON = "//span[@tabindex=0]"
AUTH_NUMBER_INPUT = "//input[@aria-required='true']"
AUTH_CODE = "//div[@aria-details='link-device-phone-number-code-screen-instructions']"
AUTH_CODE_ATTRIBUTE = 'data-link-code'
MESSAGE_INPUT = "//div[@contenteditable='true'][@data-tab='10']"
# Variables telebot
data = json.load(open('driver/telebot.json'))
API_TOKEN = data['token']
CHAT_ID = data['chatid']
PHOTO_PATH = 'image.png'


def send_photo(update: Update, context: CallbackContext):
    driver.save_screenshot(PHOTO_PATH)
    context.bot.send_photo(chat_id=CHAT_ID, photo=open(PHOTO_PATH, 'rb'))


def check_message():
    while True:
        col = db()['whatsapp']
        doc = col.find_one()
        if not doc == None:
            col.delete_one(doc)
        
            driver.get('https://web.whatsapp.com/send/?phone=' + str(doc['phone']) + '&text=' + str(doc['code']) + '%20-%20Korshiles.kz')
            
            while True:
                print('while')
                try:
                    message_input = driver.find_element("xpath", MESSAGE_INPUT)
                    time.sleep(2)
                    break
                except:
                    pass
                time.sleep(2)

            webdriver.ActionChains(driver).send_keys(webdriver.common.keys.Keys.RETURN).perform()
            print('code sent')
            time.sleep(2)
            webdriver.ActionChains(driver).send_keys(webdriver.common.keys.Keys.ESCAPE).perform()
        
        time.sleep(5)
        print('check message while')


def main():
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handler for /sendphoto
    dispatcher.add_handler(CommandHandler('sendphoto', send_photo))

    # Start the bot
    updater.start_polling()

    # Start the periodic function in a separate thread
    periodic_thread = threading.Thread(target=check_message)
    periodic_thread.start()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()