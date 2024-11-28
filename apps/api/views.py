from django.http import JsonResponse
from db import get_db_handle as db
from django.views.decorators.csrf import csrf_exempt

def index(request):
    col = db()['ads']
    doc = col.find()

    data = []
    for item in doc:
        item['_id'] = str(item['_id'])
        data.append(item)
    
    return JsonResponse(data, safe=False)


@csrf_exempt
def ad(request):
    ad = int(request.POST['ad'])
    col = db()['ads']
    doc = col.find_one({'ad': ad})
    col.update_one({'ad': ad}, {'$set': {'views': doc['views']+1}})

    doc['_id'] = str(doc['_id'])
    
    return JsonResponse(doc, safe=False)


@csrf_exempt
def filter(request):
    print(request.POST)
    print('Filter request')
    return JsonResponse('good', safe=False)