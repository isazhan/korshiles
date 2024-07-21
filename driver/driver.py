from selenium import webdriver
from chromedriver_py import binary_path
import time
import os
from pyvirtualdisplay import Display
from telegram import Bot
import asyncio
import json


display = Display(visible=0, size=(1920, 1080))
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
options.add_argument("--disable-background-networking")
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


# Variables
AUTH_BUTTON = "//span[@tabindex=0]"
AUTH_NUMBER_INPUT = "//input[@aria-required='true']"
AUTH_CODE = "//div[@aria-details='link-device-phone-number-code-screen-instructions']"
AUTH_CODE_ATTRIBUTE = 'data-link-code'


async def send_photo():
    data = json.load(open('driver/telebot.json'))
    bot = Bot(token=data['token'])
    await bot.send_photo(chat_id=data['chatid'], photo=open('image.png', 'rb'))


async def main():
    while True:
        driver.save_screenshot('image.png')
        await send_photo()
        x = input('Enter command')

        if x == 'auth_button':
            driver.find_element("xpath", AUTH_BUTTON).click()
        
        if x == 'auth_number':
            phone = input('Enter number')
            authnumber_input = driver.find_element("xpath", AUTH_NUMBER_INPUT)
            authnumber_input.send_keys(phone)
            time.sleep(2)
            authnumber_input.send_keys(webdriver.common.keys.Keys.RETURN)
            time.sleep(2)
            authcode = driver.find_element("xpath", AUTH_CODE)
            authcode = authcode.get_attribute(AUTH_CODE_ATTRIBUTE)
            print('Auth code: ' + str(authcode))

        if x == 'test_send':
            phone = input('Enter number')
            driver.get('https://web.whatsapp.com/send/?phone=' + str(phone) + '&text=test')

        if x == 'enter':
            webdriver.ActionChains(driver).send_keys(webdriver.common.keys.Keys.RETURN).perform()

        if x == 'exit':
            driver.quit()
            display.stop()
            break

        time.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())