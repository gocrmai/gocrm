from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'contact_person', 'phone', 'industry', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['shop_name', 'contact_person', 'phone', 'email']
    ordering = ['-created_at']