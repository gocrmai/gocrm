"""
Reports models for GOPOS reporting system.
"""

from django.db import models


class Store(models.Model):
    """Store/Outlet model."""
    
    name = models.CharField('店鋪名稱', max_length=200)
    location = models.CharField('地址', max_length=500, blank=True)
    is_active = models.BooleanField('啟用中', default=True)
    created_at = models.DateTimeField('創建日期', auto_now_add=True)
    
    class Meta:
        verbose_name = '店鋪'
        verbose_name_plural = '店鋪'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DailySales(models.Model):
    """Daily sales data for each store."""
    
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='daily_sales',
        verbose_name='店鋪'
    )
    date = models.DateField('日期')
    revenue = models.DecimalField('營業額', max_digits=12, decimal_places=2)
    order_count = models.IntegerField('訂單數', default=0)
    customer_count = models.IntegerField('顧客數', default=0)
    avg_order_value = models.DecimalField('平均客單', max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = '每日銷售'
        verbose_name_plural = '每日銷售'
        ordering = ['-date']
        unique_together = ['store', 'date']
    
    def __str__(self):
        return f"{self.store.name} - {self.date}"


class MonthlySummary(models.Model):
    """Monthly summary for each store."""
    
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='monthly_summaries',
        verbose_name='店鋪'
    )
    year = models.IntegerField('年份')
    month = models.IntegerField('月份')
    total_revenue = models.DecimalField('總營業額', max_digits=15, decimal_places=2)
    total_orders = models.IntegerField('總訂單數')
    total_customers = models.IntegerField('總顧客數')
    avg_daily_revenue = models.DecimalField('日均營業額', max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = '月度總結'
        verbose_name_plural = '月度總結'
        ordering = ['-year', '-month']
        unique_together = ['store', 'year', 'month']
    
    def __str__(self):
        return f"{self.store.name} - {self.year}/{self.month}"