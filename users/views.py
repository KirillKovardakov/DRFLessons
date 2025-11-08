from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import CustomUser
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer