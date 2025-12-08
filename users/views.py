from itertools import product
import json

from django.shortcuts import render
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from lms.models import Course
from .models import CustomUser, Payments
from users.serializers import UserSerializer, PaymentSerializer
from users import services


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Создаем пользователя, но не сохраняем его в базу данных
        user = serializer.validated_data
        password = user.pop('password')  # Извлекаем пароль
        # user_instance.username = user_instance.email
        user_instance = CustomUser(**user)  # Создаем экземпляр пользователя
        user_instance.set_password(password)  # Устанавливаем зашифрованный пароль
        user_instance.is_active = True  # Устанавливаем нужные поля
        user_instance.save()  # Сохраняем пользователя в базе


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        #Переводим рубли в доллары
        amount_in_dollars = services.corvert_rub_to_dollars(payment.amount)
        #Создаём оплату в долларах
        price = services.create_stripe_price(amount_in_dollars)
        #Создаём продукт
        services.create_stripe_product(payment.paid_course)
        #Создаём сессию и получаем айди сессии и ссылку на оплату
        session_id, payment_link=services.create_stripe_session(price)

        payment.session_id=session_id
        payment.link=payment_link
        payment.save()



class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'method')
    ordering_fields = ('amount',)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
