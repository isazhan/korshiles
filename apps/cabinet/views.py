from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from db import get_db_handle as db
from datetime import datetime, timedelta
import json
from PIL import Image
import os
import shutil


@login_required
def create_ad(request):
    if request.method == 'POST':
        
        data = request.POST.dict()
        
        col = db()['ads']
        doc = col.find({}, {'_id': 0, 'ad': 1}).sort('_id', -1).limit(1)
        try:
            ad = doc[0]['ad'] + 1
        except:
            ad = 100000000
        data['ad'] = ad
        data['author'] = request.user.phone_number
        data['create_time'] = datetime.now()
        data['publish'] = False
        data['views'] = 0

        z = json.load(open('static/base/cities.json', encoding='utf-8'))

        for i in z['cities']:
            if i['id'] == data['city']:
                data['city'] = {'id': data['city'], 'ru': i['ru']}
                for k in i['districts']:
                    if k['id'] == data['district']:
                        data['district'] = {'id': data['district'], 'ru': k['ru']}
                        break
                break
        
        for i in z['ad_types']:
            if i['id'] == data['type']:
                data['type'] = {'id': data['type'], 'ru': i['ru']}
                break
        
        # Photos
        images = request.FILES.getlist('photos')
        photos = []
        img_number = 1
        for i in images:
            try:
                img = Image.open(i).convert('RGB')
                os.makedirs(f'static/ads/{ad}', exist_ok=True)
                photo_path = f'static/ads/{ad}/{str(img_number) + ".webp"}'
                img.save(photo_path, format='WEBP', quality=10)
                photos.append(photo_path)
            except:
                pass
            img_number += 1
        if len(photos) > 0:
            data['photos'] = photos
        # Photos

        x = col.insert_one(data)

    return render(request, 'cabinet/create_ad.html')


@login_required
def check_ad(request):
    col = db()['ads']
    ad_go = col.find({'type.id': 'ad_go', 'publish': False})
    ad_look = col.find({'type.id': 'ad_look', 'publish': False})
    context = {
        'ad_go': ad_go,
        'ad_look': ad_look,
    }

    template = loader.get_template('cabinet/check_ad.html')
    return HttpResponse(template.render(context, request))


@login_required
def check_result(request):
    if request.method == 'POST':
        col = db()['ads']
        query = { "ad": int(request.POST['ad']) }
        if request.POST['result'] == 'accept':
            values = { "$set": { "publish": True } }
            col.update_one(query, values)
        if request.POST['result'] == 'reject':
            col.delete_one(query)
            try:
                shutil.rmtree(f'static/ads/{request.POST["ad"]}')
            except:
                pass

        return HttpResponse('success')
    

@login_required
def my_ads(request):
    col = db()['ads']

    my_ads = col.find({'author': request.user.phone_number}).sort('create_time', -1)
    context = {
        'my_ads': my_ads,
    }
    template = loader.get_template('cabinet/my_ads.html')
    return HttpResponse(template.render(context, request))


@login_required
def delete_outdated(request):
    col = db()['ads']
    query = {'create_time': {"$lt": datetime.now()-timedelta(days=7)}}
    x = col.delete_many(query)
    
    return redirect(create_ad)