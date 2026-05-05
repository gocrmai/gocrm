"""
User models for GOPOS CRM.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with Chinese name and role."""

    class Role(models.TextChoices):
        ADMIN = 'admin', '管理員'
        SUPERVISOR = 'supervisor', '主管'
        STAFF = 'staff', '員工'

    chinese_name = models.CharField('中文名', max_length=50, blank=True)
    phone = models.CharField('電話', max_length=20, blank=True)
    role = models.CharField(
        '角色',
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF
    )
    is_active = models.BooleanField('在職', default=True)
    created_at = models.DateTimeField('創建日期', auto_now_add=True)
    updated_at = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '用戶'
        verbose_name_plural = '用戶'
        ordering = ['-created_at']

    def __str__(self):
        return self.chinese_name or self.username

    def get_full_name(self):
        return self.chinese_name or self.username

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_supervisor(self):
        return self.role in [self.Role.SUPERVISOR, self.Role.ADMIN]