from django.urls import path, include


urlpatterns = [
    path('v1/faci/', include('faci.urls_api')),
    path('v1/linker/', include('django_sy_framework.linker.urls_api')),
    path('', include('django_sy_framework.base.urls_api')),
]
