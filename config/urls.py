from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('admin/', admin.site.urls),
    path('lms/', include('lms.urls', namespace='lms')),
    path('users/', include('users.urls', namespace='users')),
]
