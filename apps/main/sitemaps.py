from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from db import get_db_handle as db

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'policy', 'terms', ]

    def location(self, item):
        return reverse(item)

class DynamicViewSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        col = db()['ads']
        doc = col.find({'publish': True}, {'_id': 0, 'ad': 1})
        ads = []
        for i in doc:
            ads.append(i['ad'])

        return [
            {'name': 'ad', 'ad': i} for i in ads
        ]

    def location(self, item):

        if item['name'] == 'ad':
            return reverse('ad', kwargs={'ad': item['ad']})