from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lms.urls', namespace='lms')),
    path('', include('users.urls', namespace='users')),
]
