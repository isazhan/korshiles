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


def search(request):
    print(request.GET)
    col = db()['ads']
    doc = col.find({
        'type': request.GET['type'],
        'city': request.GET['city'],
        'district': request.GET['district'],
        '$and': [{'rental': {'$gt': request.GET['rental_from']}},
                {'rental': {'$lt': request.GET['rental_upto']}}],
    })
    context = {'doc': doc}
    template = loader.get_template('main/result.html')
    return HttpResponse(template.render(context, request))