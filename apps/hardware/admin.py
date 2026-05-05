from django.contrib import admin
from .models import Computer, Printer


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ['customer', 'model', 'hostname', 'rustdesk_id', 'warranty_expiry']
    list_filter = ['customer']
    search_fields = ['customer__shop_name', 'model', 'hostname']


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ['customer', 'model', 'name', 'ip_address']
    list_filter = ['customer']
    search_fields = ['customer__shop_name', 'model', 'name']