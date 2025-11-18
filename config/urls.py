from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lms/', include('lms.urls', namespace='lms')),
    path('users/', include('users.urls', namespace='users')),
]
