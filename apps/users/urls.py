from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup_user, name='signup'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('send_whatsapp_code', views.send_whatsapp_code, name='send_whatsapp_code'),
    path('check_authcode', views.check_authcode, name='check_authcode'),
]