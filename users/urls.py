from rest_framework.urls import app_name
from django.urls import path

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"user", UserViewSet, basename='user')
urlpatterns = [] + router.urls
