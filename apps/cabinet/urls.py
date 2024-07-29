from django.urls import path
from . import views

urlpatterns = [
    path('create_ad', views.create_ad, name='create_ad'),
    path('check_ad', views.check_ad, name='check_ad'),
    path('check_result', views.check_result, name='check_result'),
    path('my_ads', views.my_ads, name='my_ads'),
    path('delete_outdated', views.delete_outdated, name='delete_outdated'),
]