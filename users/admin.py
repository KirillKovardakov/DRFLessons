from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','country','is_superuser','is_staff')
    list_filter = ('email','country')
    search_fields = ('email','country',)