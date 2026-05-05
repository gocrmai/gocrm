"""
Hardware models for GOPOS CRM.
"""

from django.db import models
from apps.customers.models import Customer


class Computer(models.Model):
    """Computer model - stores POS computer info."""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='computers',
        verbose_name='客戶'
    )

    # Device info
    model = models.CharField('型號', max_length=200, blank=True)
    hostname = models.CharField('主機名', max_length=100, blank=True, help_text='電腦名稱')
    serial_number = models.CharField('S/N', max_length=100, blank=True)

    # Remote access
    rustdesk_id = models.CharField('Rustdesk ID', max_length=50, blank=True)
    anydesk_id = models.CharField('Anydesk ID', max_length=50, blank=True)

    # Warranty
    warranty_expiry = models.DateField('保養期', null=True, blank=True, help_text='保養到期日期')

    # Notes
    notes = models.TextField('備註', blank=True)

    # Tracking
    created_at = models.DateTimeField('創建日期', auto_now_add=True)
    updated_at = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '電腦'
        verbose_name_plural = '電腦設備'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.shop_name} - {self.model or '電腦'}"

    def is_under_warranty(self):
        """Check if device is under warranty."""
        if self.warranty_expiry:
            from django.utils import timezone
            return self.warranty_expiry >= timezone.now().date()
        return False


class Printer(models.Model):
    """Printer model - stores printer info."""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='printers',
        verbose_name='客戶'
    )

    # Device info
    model = models.CharField('型號', max_length=200, blank=True)
    name = models.CharField('名稱', max_length=100, blank=True, help_text='如：廚房打印機')
    ip_address = models.GenericIPAddressField('IP', null=True, blank=True)
    serial_number = models.CharField('S/N', max_length=100, blank=True)

    # Notes
    notes = models.TextField('備註', blank=True)

    # Tracking
    created_at = models.DateTimeField('創建日期', auto_now_add=True)
    updated_at = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '打印機'
        verbose_name_plural = '打印機設備'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.shop_name} - {self.name or self.model or '打印機'}"