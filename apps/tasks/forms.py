from django import forms
from django.forms import ModelForm
from .models import Task
from apps.customers.models import Customer
from apps.users.models import User


class TaskForm(ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        model = Task
        fields = [
            'category', 'customer', 'description', 'notes',
            'assigned_to', 'due_date', 'attachments'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'customer': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '詳細描述問題或需求...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '內部備註（對客戶不可見）...'
            }),
            'assigned_to': forms.CheckboxSelectMultiple(),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'attachments': forms.FileInput(attrs={
                'class': 'form-control',
                'multiple': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)