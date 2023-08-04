from django.contrib import admin
from .models import CustomUser, Subscription
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription)