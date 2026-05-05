from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'chinese_name', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'chinese_name', 'email']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('其他資料', {'fields': ('chinese_name', 'phone', 'role')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('其他資料', {'fields': ('chinese_name', 'phone', 'role')}),
    )