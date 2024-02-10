from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from db import get_db_handle as db


def index(request):
    return render(request, 'main/index.html')


@login_required
def create_ad(request):
    if request.method == 'POST':
        print('POST')
        print(request.POST)
        #col = db()['ads']
        #x = col.insert_one(request.POST.dict())
        return HttpResponse('ok')
    else:
        return render(request, 'main/create_ad.html')