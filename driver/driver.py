from selenium import webdriver
from chromedriver_py import binary_path
import time
import os

data = os.getcwd() + '/driver/driver-data'

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + data)

service = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://web.whatsapp.com/')

time.sleep(60)