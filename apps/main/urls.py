from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_ad', views.create_ad, name='create_ad'),
]