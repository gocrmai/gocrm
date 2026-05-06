"""
Serializers for Reports API.
"""

from rest_framework import serializers
from .models import Store, DailySales, MonthlySummary


class StoreSerializer(serializers.ModelSerializer):
    """Store serializer."""
    
    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'is_active']


class DailySalesSerializer(serializers.ModelSerializer):
    """Daily sales serializer."""
    
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = DailySales
        fields = ['id', 'store', 'store_name', 'date', 'revenue', 'order_count', 'customer_count', 'avg_order_value']


class MonthlySummarySerializer(serializers.ModelSerializer):
    """Monthly summary serializer."""
    
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = MonthlySummary
        fields = ['id', 'store', 'store_name', 'year', 'month', 'total_revenue', 'total_orders', 'total_customers', 'avg_daily_revenue']


class DashboardSummarySerializer(serializers.Serializer):
    """Dashboard summary serializer."""
    
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_orders = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    avg_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    revenue_change = serializers.DecimalField(max_digits=5, decimal_places=2)
    orders_change = serializers.DecimalField(max_digits=5, decimal_places=2)


class StorePerformanceSerializer(serializers.Serializer):
    """Store performance serializer."""
    
    store_id = serializers.IntegerField()
    store_name = serializers.CharField()
    location = serializers.CharField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    order_count = serializers.IntegerField()
    customer_count = serializers.IntegerField()
    avg_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    revenue_change = serializers.DecimalField(max_digits=5, decimal_places=2)


class TrendDataSerializer(serializers.Serializer):
    """Trend data serializer for charts."""
    
    date = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    order_count = serializers.IntegerField()
    customer_count = serializers.IntegerField()