from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
import random
from django.http import HttpResponse
from selenium import webdriver
from chromedriver_py import binary_path
from django.views.decorators.csrf import csrf_exempt
from db import get_db_handle as db
import time, os
from pyvirtualdisplay import Display


codes = {}


def login_user(request):
    print(codes)
    if request.method == 'POST':
        print(request.POST)
        phone_number = request.POST['phone_number']
        code = request.POST['code']
        password = request.POST['password']

        User = get_user_model()

        if code == '' and password == '':
            if User.objects.filter(phone_number=phone_number).exists():
                return HttpResponse('user_exist')
            else:
                print('user does not exist')
                send_whatsapp_code(phone_number)
                return HttpResponse('code_sent')
            
        if not code == '' and password == '':
            if codes[phone_number] == int(code):
                return HttpResponse('code_accept')
            else:
                return HttpResponse('code_wrong')
        
        if code == '' and not password == '':
            if User.objects.filter(phone_number=phone_number).exists():
                user = authenticate(phone_number=phone_number, password=password)
            else:
                user = User.objects.create_user(phone_number, password)
                user.save()
            login(request, user)
            return HttpResponse('login')
        
    else:
        return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('/')



def send_whatsapp_code(phone_number):
    code = random.randint(1000,9999)
    codes[phone_number] = code
    print('code created')
    # Start Chromedriver
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    print('display start')
    options = webdriver.ChromeOptions()
    data = os.getcwd() + '/driver/driver-data'
    options.add_argument('--user-data-dir=' + data)
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
    text = str(code)

    driver.get('https://web.whatsapp.com/send/?phone=' + str(phone_number) + '&text=' + text)
    print('url setted')

    while True:
        print('while')
        try:
            MESSAGE_INPUT = "//div[@contenteditable='true'][@data-tab='10']"
            message_input = driver.find_element("xpath", MESSAGE_INPUT)
            time.sleep(2)
            break
        except:
            pass
        time.sleep(2)

    webdriver.ActionChains(driver).send_keys(webdriver.common.keys.Keys.RETURN).perform()
    print('code sent')
    time.sleep(10)
    driver.quit()
    display.stop()