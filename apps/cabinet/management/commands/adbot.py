from django.core.management.base import BaseCommand
from telethon import TelegramClient, events
import json
from google import genai
from db import get_db_handle as db
from datetime import datetime
from groq import Groq


data = json.load(open('adbot.json'))
API_ID = data['api_id']
API_HASH = data['api_hash']
GEMINI_API_KEY = data['gemini_api_key']
GROQ_API_KEY = data['groq_api_key']

# Можно указывать username (например, 'pythontext') или ID каналов (-100xxxxxxxxx)
CHANNELS_TO_LISTEN = [
    -1001365122823, 
    -1002909230162,
]

# Создаем клиента. При первом запуске скрипт попросит ввести номер телефона и код из Telegram
client = TelegramClient('session_listener', API_ID, API_HASH)

client_gemini = genai.Client(api_key=GEMINI_API_KEY)
client_groq = Groq(api_key=GROQ_API_KEY)

# Одиночные сообщения
@client.on(events.NewMessage(chats=CHANNELS_TO_LISTEN))
async def handler(event):
    if event.message.grouped_id is not None:
        return
    
    message_text = event.message.message
    if message_text:
        if event.message.photo:
            await gemini(message_text, event.message)
        else:
            await gemini(message_text)


# Альбомные сообщения
@client.on(events.Album(chats=CHANNELS_TO_LISTEN))
async def album_handler(event):
    message_text = event.text
    if message_text:
        await gemini(message_text, event.messages)


async def gemini(message_text, photo=None):
    contents="""Посмотри нижний текст. Если это объявление на подселение в Алматы и есть контактный номер телефона, тогда верни мне json с следующими полями:
            1) "type": если это "ищу на подселение" тогда значение "ad_look", а если "пойду на подселение" тогда значение "ad_go". Если трудно понять ставь ad_look.
            2) "district": Алатауский "101", Алмалинский "102", Ауэзовский "103", Бостандыкский "104", Жетысуский "105", Медеуский "106", Наурызбайский "107", Турксибский "108". Если трудно понять оставь пустым.
            3) "address": попробуй вытащить адрес в виде текста, если не получается оставь пустым.
            4) "contact": вытащи номер телефона в формате 77XXXXXXXXX. Только 11 цифр и всегда должен начинаться на 7. Это обязательно должно быть в объявлении, если не получается найти, тогда не возвращай json.
            Все значения string.""" + "\n\n" + str(message_text)
    try:
        # Gemini
        """
        response = client_gemini.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=contents,
        )
        ad_data = response.text
        """

        # Groq
        chat_completion = client_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": contents,
                }
            ],
            model="openai/gpt-oss-20b",
        )
        ad_data = chat_completion.choices[0].message.content

        #print(type(ad_data))
        #print(ad_data)
        clean_json = ad_data.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        #print("json успешно создан")
        
        # Create ad
        await create_ad(data, message_text, photo)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def create_ad(data, message_text, photo):
    #print("создание объявления")
    col = db()['ads']
    doc = col.find({}, {'_id': 0, 'ad': 1}).sort('_id', -1).limit(1)
    try:
        ad = doc[0]['ad'] + 1
    except:
        ad = 100000000
    data['ad'] = ad
    data['author'] = data['contact']
    data['create_time'] = datetime.now()
    data['publish'] = False
    data['views'] = 0
    data['info'] = str(message_text)
    data['city'] = '1'
    z = json.load(open('static/base/cities.json', encoding='utf-8'))
    for i in z['cities']:
        if i['id'] == data['city']:
            data['city'] = {'id': data['city'], 'kk': i['kk'], 'ru': i['ru']}
            for k in i['districts']:
                if k['id'] == data['district']:
                    data['district'] = {'id': data['district'], 'kk': k['kk'], 'ru': k['ru']}
                    break
            break
    
    for i in z['ad_types']:
        if i['id'] == data['type']:
            data['type'] = {'id': data['type'], 'kk': i['kk'], 'ru': i['ru']}
            break


    y = await photo_download(photo, ad)
    if y is not None:
        data['photos'] = y
    #print(data)
    x = col.insert_one(data)

async def photo_download(photo, ad):
    photos = []
    if not photo:
        return None
    
    if not isinstance(photo, list):
        if photo.photo:
            photo_path = await client.download_media(photo, file=f'static/ads/{ad}/')
            if photo_path:
                photos.append(photo_path)
    else:
        for message in photo:
            if message.photo:
                photo_path = await client.download_media(message, file=f'static/ads/{ad}/')
                if photo_path:
                    photos.append(photo_path)

    return photos


async def main():
    #print("Бот запущен и слушает указанные каналы...")
    await client.run_until_disconnected()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with client:
            client.loop.run_until_complete(main())