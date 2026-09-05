from django.contrib.syndication.views import Feed
from db import get_db_handle as db
from . import views


class CustomDataFeed(Feed):
    title = "RSS-лента из внешнего источника"
    link = "/rss/"
    description = "Лента новостей, собранная без использования моделей Django ORM."

    def items(self):
        col = db()['ads']
        ads = col.find({'publish': True}).sort('create_time', -1).limit(100)
        
        return ads
    
    def item_title(self, item):
        return item["type"]['ru']

    def item_description(self, item):
        return item["info"]

    def item_link(self, item):
        return f'/ad/{item["ad"]}'

    def item_pubdate(self, item):
        return item["create_time"]