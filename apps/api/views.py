from django.http import JsonResponse
from db import get_db_handle as db


def index(request):
    col = db()['ads']
    doc = col.find()

    data = []
    for item in doc:
        item['_id'] = str(item['_id'])
        data.append(item)
    
    return JsonResponse(data, safe=False)