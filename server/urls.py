from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('faci/', include('faci.urls')),
    path('auth/', include('custom_auth.urls')),
    path('', include('pages.urls')),
    path('api/', include('server.urls_api')),
]
