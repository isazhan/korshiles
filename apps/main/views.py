from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from db import get_db_handle as db


def index(request):
    col = db()['ads']
    ad_go = col.find({'type': 'ad_go'}).limit(10)
    ad_looking = col.find({'type': 'ad_looking'}).limit(10)
    context = {
        'ad_go': ad_go,
        'ad_looking': ad_looking,
    }

    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context, request))


@login_required
def create_ad(request):
    if request.method == 'POST':
        print('POST')
        print(request.POST)
        col = db()['ads']
        x = col.insert_one(request.POST.dict())
        return index(request)
    else:
        return render(request, 'main/create_ad.html')