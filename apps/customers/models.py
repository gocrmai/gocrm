"""
Customer models for GOPOS CRM.
"""

from django.db import models
from django.urls import reverse


class Customer(models.Model):
    """Customer model - stores restaurant client information."""

    class Industry(models.TextChoices):
        RESTAURANT = 'restaurant', '餐廳'
        CAFE = 'cafe', '咖啡店'
        BAR = 'bar', '酒吧'
        FAST_FOOD = 'fast_food', '快餐店'
        DIM_SUM = 'dim_sum', '酒樓/点心'
        WESTERN = 'western', '西餐'
        JAPANESE = 'japanese', '日本料理'
        CHINESE = 'chinese', '中菜'
        OTHER = 'other', '其他'

    # Basic Information
    shop_name = models.CharField('店名', max_length=200)
    contact_person = models.CharField('聯絡人', max_length=100)
    phone = models.CharField('電話', max_length=20)
    email = models.EmailField('電郵', blank=True)
    address = models.TextField('地址', blank=True)
    industry = models.CharField(
        '行業',
        max_length=50,
        choices=Industry.choices,
        default=Industry.RESTAURANT
    )

    # Software products (multiple selection stored as comma-separated)
    software = models.CharField('軟件', max_length=500, blank=True, help_text='GOPOS/M3/QR/POS6/外賣對接')

    # Hardware info
    hardware = models.CharField('硬體', max_length=500, blank=True, help_text='主要設備型號')

    # Other info
    other = models.TextField('其他', blank=True, help_text='其他備註')
    notes = models.TextField('備註', blank=True, help_text='內部備註')

    # Tracking
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_customers',
        verbose_name='創建人'
    )
    created_at = models.DateTimeField('創建日期', auto_now_add=True)
    updated_at = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '客戶'
        verbose_name_plural = '客戶資料'
        ordering = ['-created_at']

    def __str__(self):
        return self.shop_name

    def get_absolute_url(self):
        return reverse('customer_detail', kwargs={'pk': self.pk})

    def get_software_list(self):
        """Return software list as Python list."""
        if self.software:
            return [s.strip() for s in self.software.split(',') if s.strip()]
        return []

    def get_tasks(self):
        """Get all tasks for this customer."""
        from apps.tasks.models import Task
        return Task.objects.filter(customer=self)

    def get_hardware(self):
        """Get all hardware for this customer."""
        from apps.hardware.models import Computer, Printer
        computers = Computer.objects.filter(customer=self)
        printers = Printer.objects.filter(customer=self)
        return {'computers': computers, 'printers': printers}