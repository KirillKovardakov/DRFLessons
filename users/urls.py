from rest_framework.urls import app_name
from django.urls import path

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users import views

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"user", views.UserViewSet, basename='user')
urlpatterns = [
                  path('payment/create/', views.PaymentCreateAPIView.as_view(), name='payment-create'),
                  path('payment/', views.PaymentListAPIView.as_view(), name='payment-list'),
                  path('payment/<int:pk>/', views.PaymentRetrieveAPIView.as_view(), name='payment-get'),
                  path('payment/delete/<int:pk>/', views.PaymentDestroyAPIView.as_view(), name='payment-delete'),
                  path('payment/update/<int:pk>/', views.PaymentUpdateAPIView.as_view(), name='payment-update'),
              ] + router.urls
