from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from db import get_db_handle as db
import time


@login_required
def create_ad(request):
    if request.method == 'POST':
        print('POST')
        print(request.POST)
        data = request.POST.dict()
        col = db()['ads']
        doc = col.find({}, {'_id': 0, 'ad': 1}).sort('_id', -1).limit(1)
        try:
            ad = doc[0]['ad'] + 1
        except:
            ad = 100000000
        data['ad'] = ad
        data['author'] = request.user.phone_number
        data['create_time'] = time.time()
        data['publish'] = False
        x = col.insert_one(data)
    return render(request, 'cabinet/create_ad.html')


@login_required
def check_ad(request):
    col = db()['ads']
    doc = col.find({'publish': False})
    context = {'doc': doc}
    template = loader.get_template('cabinet/check_ad.html')
    return HttpResponse(template.render(context, request))