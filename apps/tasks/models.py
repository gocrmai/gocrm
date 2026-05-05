"""
Task models for GOPOS CRM.
"""

from django.db import models
from django.contrib.auth import get_user_model
from apps.customers.models import Customer


class Task(models.Model):
    """Task model - work orders for customers."""

    class Category(models.TextChoices):
        INSTALLATION = 'installation', '安裝'
        REPAIR = 'repair', '維修'
        MENU_UPDATE = 'menu_update', '餐牌修改'
        SYSTEM_REQUEST = 'system_request', '系統需求'
        ONSITE_SERVICE = 'onsite_service', '上門服務'
        OTHER = 'other', '其他'

    class Status(models.TextChoices):
        PENDING = 'pending', '待處理'
        RECEIVED = 'received', '已接收'
        IN_PROGRESS = 'in_progress', '處理中'
        COMPLETED = 'completed', '已完成'
        CANCELLED = 'cancelled', '已取消'

    # Task identification
    task_number = models.CharField('任務編號', max_length=50, unique=True)
    category = models.CharField('分類', max_length=30, choices=Category.choices)
    status = models.CharField('進度', max_length=20, choices=Status.choices, default=Status.PENDING)

    # Customer info
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='客戶'
    )

    # Task details
    description = models.TextField('事項描述')
    notes = models.TextField('備註', blank=True)

    # Assignment
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
        verbose_name='創建人'
    )
    assigned_to = models.ManyToManyField(
        get_user_model(),
        related_name='assigned_tasks',
        verbose_name='指派給',
        blank=True
    )

    # Dates
    created_at = models.DateTimeField('創建日期', auto_now_add=True)
    updated_at = models.DateTimeField('更新日期', auto_now=True)
    due_date = models.DateField('指定完成日期', null=True, blank=True)
    completed_at = models.DateTimeField('完成日期', null=True, blank=True)

    # Attachments
    attachments = models.FileField(
        '附件',
        upload_to='tasks/%Y/%m/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = '任務'
        verbose_name_plural = '工作紀錄'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.task_number} - {self.customer.shop_name}"

    def save(self, *args, **kwargs):
        if not self.task_number:
            # Generate task number: GOPOS-YYYYMMDD-XXX
            from datetime import date
            today = date.today().strftime('%Y%m%d')
            last_task = Task.objects.filter(
                task_number__startswith=f'GOPOS-{today}'
            ).order_by('-task_number').first()

            if last_task:
                last_number = int(last_task.task_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.task_number = f"GOPOS-{today}-{new_number:03d}"

        super().save(*args, **kwargs)

    def get_category_display_class(self):
        """Return CSS class for category badge."""
        mapping = {
            'installation': 'bg-primary',
            'repair': 'bg-danger',
            'menu_update': 'bg-warning',
            'system_request': 'bg-info',
            'onsite_service': 'bg-success',
            'other': 'bg-secondary',
        }
        return mapping.get(self.category, 'bg-secondary')

    def get_status_display_class(self):
        """Return CSS class for status badge."""
        mapping = {
            'pending': 'badge-secondary',
            'received': 'badge-info',
            'in_progress': 'badge-primary',
            'completed': 'badge-success',
            'cancelled': 'badge-danger',
        }
        return mapping.get(self.status, 'badge-secondary')