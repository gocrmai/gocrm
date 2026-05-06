"""
Views for Reports API.
"""

from django.db.models import Sum, Avg, Count
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Store, DailySales, MonthlySummary
from .serializers import (
    StoreSerializer,
    DailySalesSerializer,
    MonthlySummarySerializer,
    DashboardSummarySerializer,
    StorePerformanceSerializer,
    TrendDataSerializer
)


class DashboardView(APIView):
    """Dashboard API - returns overview statistics."""
    
    def get(self, request):
        # Get date range from query params
        days = int(request.query_params.get('days', 7))
        store_ids = request.query_params.get('stores', '')  # comma separated
        
        today = timezone.now().date()
        start_date = today - timedelta(days=days-1)
        previous_start = start_date - timedelta(days=days)
        
        # Build queryset
        queryset = DailySales.objects.filter(date__gte=start_date, date__lte=today)
        
        if store_ids:
            store_list = [int(x) for x in store_ids.split(',') if x.isdigit()]
            queryset = queryset.filter(store_id__in=store_list)
        
        # Current period totals
        current_totals = queryset.aggregate(
            total_revenue=Coalesce(Sum('revenue'), 0),
            total_orders=Coalesce(Sum('order_count'), 0),
            total_customers=Coalesce(Sum('customer_count'), 0)
        )
        
        # Calculate avg order value
        total_revenue = current_totals['total_revenue'] or 0
        total_orders = current_totals['total_orders'] or 0
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Previous period for comparison
        previous_qs = DailySales.objects.filter(
            date__gte=previous_start,
            date__lt=start_date
        )
        if store_ids:
            previous_qs = previous_qs.filter(store_id__in=store_list)
        
        previous_totals = previous_qs.aggregate(
            total_revenue=Coalesce(Sum('revenue'), 0),
            total_orders=Coalesce(Sum('order_count'), 0)
        )
        
        # Calculate changes
        prev_revenue = previous_totals['total_revenue'] or 0
        prev_orders = previous_totals['total_orders'] or 0
        
        revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
        orders_change = ((total_orders - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0
        
        data = {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_customers': current_totals['total_customers'],
            'avg_order_value': avg_order_value,
            'revenue_change': revenue_change,
            'orders_change': orders_change
        }
        
        serializer = DashboardSummarySerializer(data)
        return Response(serializer.data)


class StoreListView(APIView):
    """Store list API."""
    
    def get(self, request):
        stores = Store.objects.filter(is_active=True)
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)


class StorePerformanceView(APIView):
    """Store performance API - returns today's sales for all stores."""
    
    def get(self, request):
        today = timezone.now().date()
        store_ids = request.query_params.get('stores', '')
        
        queryset = DailySales.objects.filter(date=today)
        if store_ids:
            store_list = [int(x) for x in store_ids.split(',') if x.isdigit()]
            queryset = queryset.filter(store_id__in=store_list)
        
        # Calculate change vs yesterday
        yesterday = today - timedelta(days=1)
        
        result = []
        for sale in queryset.select_related('store'):
            prev_sale = DailySales.objects.filter(store=sale.store, date=yesterday).first()
            
            prev_revenue = prev_sale.revenue if prev_sale else 0
            revenue_change = ((sale.revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            
            result.append({
                'store_id': sale.store.id,
                'store_name': sale.store.name,
                'location': sale.store.location,
                'revenue': sale.revenue,
                'order_count': sale.order_count,
                'customer_count': sale.customer_count,
                'avg_order_value': sale.avg_order_value,
                'revenue_change': revenue_change
            })
        
        # Sort by revenue descending
        result.sort(key=lambda x: x['revenue'], reverse=True)
        
        serializer = StorePerformanceSerializer(result, many=True)
        return Response(serializer.data)


class TrendView(APIView):
    """Trend API - returns daily sales for chart."""
    
    def get(self, request):
        days = int(request.query_params.get('days', 7))
        store_ids = request.query_params.get('stores', '')
        
        today = timezone.now().date()
        start_date = today - timedelta(days=days-1)
        
        queryset = DailySales.objects.filter(
            date__gte=start_date,
            date__lte=today
        )
        
        if store_ids:
            store_list = [int(x) for x in store_ids.split(',') if x.isdigit()]
            queryset = queryset.filter(store_id__in=store_list)
        
        # Aggregate by date
        daily_data = queryset.values('date').annotate(
            revenue=Sum('revenue'),
            order_count=Sum('order_count'),
            customer_count=Sum('customer_count')
        ).order_by('date')
        
        result = []
        for item in daily_data:
            result.append({
                'date': item['date'],
                'revenue': item['revenue'],
                'order_count': item['order_count'],
                'customer_count': item['customer_count']
            })
        
        serializer = TrendDataSerializer(result, many=True)
        return Response(serializer.data)


class MonthlyOverviewView(APIView):
    """Monthly overview API."""
    
    def get(self, request):
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        store_ids = request.query_params.get('stores', '')
        
        queryset = MonthlySummary.objects.filter(year=year, month=month)
        if store_ids:
            store_list = [int(x) for x in store_ids.split(',') if x.isdigit()]
            queryset = queryset.filter(store_id__in=store_list)
        
        serializer = MonthlySummarySerializer(queryset, many=True)
        return Response(serializer.data)


def reports_dashboard(request):
    """Reports dashboard page."""
    from django.shortcuts import render
    return render(request, 'reports/dashboard.html')