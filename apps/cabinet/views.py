from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from db import get_db_handle as db
from datetime import datetime, timedelta
import json
from PIL import Image
from io import BytesIO
import base64


@login_required
def create_ad(request):
    if request.method == 'POST':
        
        data = request.POST.dict()

        # Photos
        images = request.FILES.getlist('photos')
        results = []
        for image in images:
            try:
                img = Image.open(image).convert('RGB')
                webp_data = None

                for quality in range(80, 10, -10):
                    try:
                        buffer = BytesIO()
                        img.save(buffer, format='WEBP', quality=quality)
                        img_data = buffer.getvalue()
                        
                        if len(img_data) < 100*1024 or quality==10: # 500 KB
                            webp_data = img_data
                            break

                    except:
                        pass

                encoded_image = base64.b64encode(webp_data).decode('utf-8')
                results.append(encoded_image)

            except:
                pass
        # Photos
        print(len(results))

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
        data['photos'] = results

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