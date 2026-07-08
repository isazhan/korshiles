from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

handler404 = 'apps.main.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my/', include('apps.users.urls')),
    path('', include('apps.main.urls')),
    path('cabinet/', include('apps.cabinet.urls')),
    path('api/', include('apps.api.urls')),
]
