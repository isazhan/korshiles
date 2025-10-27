from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    # Common
    path('index', views.index, name='index'),
    path('api_my_ads', views.my_ads, name='api_my_ads'),
    path('ad', views.ad, name='ad'),
    path('api_create_ad', views.CreateAdAPIView.as_view(), name='api_create_ad'),

    # Login Views
    path('api_login', views.LoginAPIView.as_view(), name='api_login'),
    path('api_logout', TokenBlacklistView.as_view(), name='api_logout'),
    path('api_delete_account', views.DeleteAccountAPIView.as_view(), name='api_delete_account'),

    # JWT Views
    path('api_get_token', TokenObtainPairView.as_view(), name='api_get_token'),
    path('api_refresh_token', TokenRefreshView.as_view(), name='api_refresh_token'),
    path('api_check_token', views.CheckTokenAPIView.as_view(), name='api_check_token'),
]