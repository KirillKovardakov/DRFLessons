from rest_framework.serializers import ModelSerializer
from .models import CustomUser, Payments


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = ['user', 'paid_course', 'paid_lesson', 'amount', 'method', ]


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'country', 'payments', ]
