from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_number', 'category', 'customer', 'status', 'created_at', 'due_date']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['task_number', 'customer__shop_name', 'description']
    ordering = ['-created_at']
    filter_horizontal = ['assigned_to']