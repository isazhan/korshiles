from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from db import get_db_handle as db

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', ]

    def location(self, item):
        return reverse(item)

class DynamicViewSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        col = db()['ads']
        doc = col.find({}, {'_id': 0, 'ad': 1}).sort('_id', -1).limit(1)
        try:
            last_ad = doc[0]['ad'] + 1
        except:
            last_ad = 100000000

        return [
            {'name': 'ad', 'ad': i} for i in range(100000000, last_ad)
        ]

    def location(self, item):

        if item['name'] == 'ad':
            return reverse('ad', kwargs={'ad': item['ad']})