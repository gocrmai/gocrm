from django.contrib import admin
from .models import Store, DailySales, MonthlySummary


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'location']


@admin.register(DailySales)
class DailySalesAdmin(admin.ModelAdmin):
    list_display = ['store', 'date', 'revenue', 'order_count', 'customer_count']
    list_filter = ['store', 'date']
    search_fields = ['store__name']
    date_hierarchy = 'date'


@admin.register(MonthlySummary)
class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ['store', 'year', 'month', 'total_revenue', 'total_orders']
    list_filter = ['store', 'year', 'month']