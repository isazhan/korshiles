from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('ad', views.ad, name='ad'),
    path('filter', views.filter, name='filter'),
]