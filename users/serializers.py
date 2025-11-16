from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import CustomUser, Payments


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = ['id', 'user', 'paid_course', 'paid_lesson', 'amount', 'method', ]


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'country', 'payments', 'is_active', 'user_permissions', 'password',]
        # fields='__all__'
