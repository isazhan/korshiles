from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, DynamicViewSitemap


sitemaps = {
    'static': StaticViewSitemap,
    'dynamic': DynamicViewSitemap,
}


urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('ad/<int:ad>', views.ad, name='ad'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', views.robots_txt),
]