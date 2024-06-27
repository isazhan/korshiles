from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib import messages
import random
from django.http import HttpResponse
from selenium import webdriver
from chromedriver_py import binary_path
from django.views.decorators.csrf import csrf_exempt
from db import get_db_handle as db

'''
def signup_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
'''
auth_codes = {}

def signup_user(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        auth_code = random.randint(1000,9999)
        auth_codes[phone_number] = auth_code
        print(auth_codes)
        # Send whatsapp code
        #send_whatsapp_code(phone_number, auth_code)
        return HttpResponse('code_sent')
    return render(request, 'users/signup.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def send_whatsapp_code(request):
    print(request)
    if request.method == 'POST':
        phonenumber = request.POST['phonenumber']
        authcode = random.randint(1000,9999)
        print(authcode)

        col = db()['authcode']
        data = {
            'phonenumber': phonenumber,
            'authcode': authcode,
        }
        x = col.insert_one(data)
        '''
        # Start Chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument('incognito')
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('user-agent=User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

        service = webdriver.ChromeService(executable_path=binary_path)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get('https://web.whatsapp.com/')

        webdriver.ActionChains(driver).send_keys(webdriver.common.keys.Keys.RETURN).perform()
        '''
        return HttpResponse(authcode)


def check_authcode(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        auth_code = request.POST['auth_code']
        password = request.POST['password']

        if auth_codes[phone_number] == auth_code:
            user = CustomUser.objects.create_user(phone_number=phone_number, password=password)
            del auth_codes[phone_number]
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse('invalid_code')