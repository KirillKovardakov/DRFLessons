from django.contrib import admin
from .models import CustomUser, Payments

@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','country','is_superuser','is_staff', 'is_active', 'last_login')
    list_filter = ('email','country')
    search_fields = ('email','country',)

    @admin.register(Payments)
    class PaymentsAdmin(admin.ModelAdmin):
        list_display = ('user', 'created_at', 'paid_course', 'paid_lesson', 'amount', 'method')
        list_filter = ('user', 'paid_course', 'paid_lesson', 'amount', 'method')
        search_fields = ('user', 'created_at', 'paid_course', 'paid_lesson', 'amount', 'method',)