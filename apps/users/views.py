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
        password_new = request.POST['password_new']

        User = get_user_model()

        if code == '' and password == '' and password_new == '':
            if User.objects.filter(phone_number=phone_number).exists():
                return HttpResponse('user_exist')
            else:
                print('user does not exist')
                send_whatsapp_code(phone_number)
                return HttpResponse('code_sent')
            
        if not code == '' and password == '' and password_new == '':
            if codes[phone_number] == int(code):
                return HttpResponse('code_accept')
            else:
                return HttpResponse('code_wrong')
        
        if code == '' and not password == '' or not password_new == '':
            if User.objects.filter(phone_number=phone_number).exists():
                user = authenticate(phone_number=phone_number, password=password)
            else:
                user = User.objects.create_user(phone_number, password_new)
                user.save()
            try:
                login(request, user)
            except:
                return HttpResponse('password_wrong')
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
    col = db()['whatsapp']
    x = col.insert_one({'phone': phone_number, 'code': code})


def forget_password(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        User = get_user_model()
        user = User.objects.get(phone_number=phone_number)
        user.delete()
        return HttpResponse('user_deleted')