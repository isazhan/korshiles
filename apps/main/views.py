from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from db import get_db_handle as db


def index(request):
    col = db()['ads']
    ad_go = col.find({'type': 'ad_go', 'publish': True}).limit(10).sort('create_time', -1)
    ad_look = col.find({'type': 'ad_look', 'publish': True}).limit(10).sort('create_time', -1)
    context = {
        'ad_go': ad_go,
        'ad_look': ad_look,
    }

    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context, request))


def search(request):
    print('Request')
    print(request.GET)
    data = request.GET.dict()
    print(data)
    filter_dict = {}
    for key, value in data.items():
        if key.endswith('_min') or key.endswith('_max'):
            field, range_type = key.rsplit('_', 1)
            if field not in filter_dict:
                filter_dict[field] = {}
            if not value == '':
                if range_type == 'min':
                    filter_dict[field]['$gte'] = int(value)
                elif range_type == 'max':
                    filter_dict[field]['$lte'] = int(value)
        elif key=='city' or key=='district':
            if not value == '':
                filter_dict[key+'.id'] = value
        else:
            if not value == '':
                filter_dict[key] = value
    print('Filter')
    print(filter_dict)
    col = db()['ads']
    doc = col.find(filter_dict).sort('create_time', -1)
    context = {'doc': doc}
    template = loader.get_template('main/result.html')
    return HttpResponse(template.render(context, request))


def ad(request, ad):
    col = db()['ads']
    doc = col.find_one({'ad': ad})
    if doc['publish'] == False and request.user.is_staff == False:
        return redirect(index)
    else:
        col.update_one({'ad': ad}, {'$set': {'views': doc['views']+1}})
        context = {'doc': doc}
        template = loader.get_template('main/ad.html')
        return HttpResponse(template.render(context, request))
    

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: ",
        "",
        "Sitemap: https://korshiles.kz/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")