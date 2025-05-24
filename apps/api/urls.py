from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('index', views.index, name='index'),
    path('ad', views.ad, name='ad'),
    path('api_create_ad', views.CreateAdAPIView.as_view(), name='api_create_ad'),
    path('api_login', views.LoginAPIView.as_view(), name='api_login'),
    path('api_logout', views.LogoutAPIView.as_view(), name='api_logout'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]