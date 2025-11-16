from rest_framework.decorators import permission_classes
from rest_framework.urls import app_name
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    # User
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('list/', views.UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user-get'),
    path('delete/<int:pk>/', views.UserDestroyAPIView.as_view(), name='user-delete'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-update'),
    # Payment
    path('payment/create/', views.PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/', views.PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/<int:pk>/', views.PaymentRetrieveAPIView.as_view(), name='payment-get'),
    path('payment/delete/<int:pk>/', views.PaymentDestroyAPIView.as_view(), name='payment-delete'),
    path('payment/update/<int:pk>/', views.PaymentUpdateAPIView.as_view(), name='payment-update'),
]
