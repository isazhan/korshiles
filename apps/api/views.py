from django.http import JsonResponse
from db import get_db_handle as db
from django.views.decorators.csrf import csrf_exempt

def index(request):
    #print('Index request: ', request.GET)

    data = request.GET.dict()
    #print(data)
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
        elif key=='city' or key=='district' or key=='type':
            if not value == '':
                filter_dict[key+'.id'] = value
        else:
            if not value == '':
                filter_dict[key] = value
    #print('Filter')
    #print(filter_dict)
    col = db()['ads']
    doc = col.find(filter_dict).sort('create_time', -1)

    data = []
    for item in doc:
        item['_id'] = str(item['_id'])
        data.append(item)

    return JsonResponse(data, safe=False)


@csrf_exempt
def ad(request):
    ad = int(request.GET['ad'])
    col = db()['ads']
    doc = col.find_one({'ad': ad})
    col.update_one({'ad': ad}, {'$set': {'views': doc['views']+1}})

    doc['_id'] = str(doc['_id'])

    return JsonResponse(doc, safe=False)