"""
URL configuration for Reports API.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('api/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/stores/', views.StoreListView.as_view(), name='store_list'),
    path('api/performance/', views.StorePerformanceView.as_view(), name='store_performance'),
    path('api/trend/', views.TrendView.as_view(), name='trend'),
    path('api/monthly/', views.MonthlyOverviewView.as_view(), name='monthly'),
]