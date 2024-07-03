from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from db import get_db_handle as db


@login_required
def create_ad(request):
    if request.method == 'POST':
        print('POST')
        print(request.POST)
        col = db()['ads']
        x = col.insert_one(request.POST.dict())
        return render(request, 'cabinet/create_ad.html')
    else:
        return render(request, 'cabinet/create_ad.html')