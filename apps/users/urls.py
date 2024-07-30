from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('send_whatsapp_code', views.send_whatsapp_code, name='send_whatsapp_code'),
]