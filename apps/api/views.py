from django.http import JsonResponse
from db import get_db_handle as db
from django.views.decorators.csrf import csrf_exempt
import random
import telebot
import json
from datetime import datetime, timedelta

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
        #else:
            #if not value == '':
                #filter_dict[key] = value
    #print('Filter')
    #print(filter_dict)
    filter_dict['publish'] = True

    quantity_in_page = 10
    start = int(data['page']) * quantity_in_page - quantity_in_page
    #print('Start: ', start)
    col = db()['ads']
    doc = col.find(filter_dict).skip(start).limit(quantity_in_page).sort('create_time', -1)
    

    ads = []
    for item in doc:
        item['_id'] = str(item['_id'])
        ads.append(item)
    
    data = {
        'ads': ads,
        #'page': int(data['page']),
        #'quantity_in_page': quantity_in_page,
        'total': col.count_documents(filter_dict)
    }
    
    #print(data)

    return JsonResponse(data, safe=False)


def my_ads(request):
    phone_number = request.GET['phone_number']
    col = db()['ads']
    query = {'author': phone_number}
    doc = col.find(query).sort('create_time', -1)

    ads = []
    for item in doc:
        item['_id'] = str(item['_id'])
        ads.append(item)
    
    data = {
        'ads': ads,
    }

    return JsonResponse(data, safe=False)
    

@csrf_exempt
def ad(request):
    ad = int(request.GET['ad'])
    col = db()['ads']
    doc = col.find_one({'ad': ad})
    col.update_one({'ad': ad}, {'$set': {'views': doc['views']+1}})

    doc['_id'] = str(doc['_id'])

    return JsonResponse(doc, safe=False)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.permissions import IsAuthenticated

codes = {}

class LoginAPIView(APIView):
    def post(self, request):
        #print('Login request: ', request.data)
        phone_number = request.data['phone_number']
        code = request.data['code']
        password = request.data['password']
        password_new = request.data['password_new']

        User = get_user_model()

        if code == '' and password == '' and password_new == '':
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'status': 'user_exist'})
            else:
                print('user does not exist')
                send_code(phone_number)
                return JsonResponse({'status': 'code_sent'})
        
        if not code == '' and password == '' and password_new == '':
            if codes[phone_number] == int(code):
                return JsonResponse({'status': 'code_accept'})
            else:
                return JsonResponse({'status': 'code_wrong'})
            
        if code == '' and not password == '' or not password_new == '':
            if User.objects.filter(phone_number=phone_number).exists():
                user = authenticate(phone_number=phone_number, password=password)
            else:
                user = User.objects.create_user(phone_number, password_new)
                user.save()
            if user and user.is_active:
                #user = serializer.validated_data['user']
                login(request, user)
                #serializer = LoginSerializer(data=request.data)
                #serializer.is_valid(raise_exception=True)
                #user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'status': 'login',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data,
                })
            else:
                return JsonResponse({'status': 'password_wrong'})
            return JsonResponse({'status': 'login'})
        '''
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
        })
        '''

class CheckTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response('success')


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    

class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.user.phone_number
        User = get_user_model()
        user = User.objects.get(phone_number=phone_number)
        user.delete()
        return Response({'status': 'ok'})



def send_code(phone_number):
    code = random.randint(1000,9999)
    codes[phone_number] = code

    data = json.load(open('telebot.json'))
    API_TOKEN = data['token']
    col = db()['telebot']
    query = {'phone': phone_number}
    doc = col.find_one(query)
    CHAT_ID = doc['chatid']
    bot = telebot.TeleBot(API_TOKEN)
    bot.send_message(CHAT_ID, 'Ваш код подтверждения - '+str(code))


class CreateAdAPIView(APIView):

    def post(self, request):
        data = request.data
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

        x = col.insert_one(data)

        return JsonResponse({'status': 'ok'})