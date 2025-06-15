from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('index', views.index, name='index'),
    path('api_my_ads', views.my_ads, name='api_my_ads'),
    path('ad', views.ad, name='ad'),
    path('api_create_ad', views.CreateAdAPIView.as_view(), name='api_create_ad'),
    path('api_login', views.LoginAPIView.as_view(), name='api_login'),
    path('api_logout', views.LogoutAPIView.as_view(), name='api_logout'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api_check_token', views.CheckTokenAPIView.as_view(), name='api_check_token'),
]