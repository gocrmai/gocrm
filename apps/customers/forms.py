from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    """Form for creating and editing customers."""

    class Meta:
        model = Customer
        fields = [
            'shop_name', 'contact_person', 'phone', 'email', 'address',
            'industry', 'software', 'hardware', 'other', 'notes'
        ]
        widgets = {
            'shop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '店名'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '聯絡人姓名'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '電話號碼'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '電郵地址'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '餐廳地址'
            }),
            'industry': forms.Select(attrs={'class': 'form-select'}),
            'software': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GOPOS/M3/QR/POS6/外賣對接（用逗號分隔）'
            }),
            'hardware': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '主要設備型號'
            }),
            'other': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '其他備註'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '內部備註'
            }),
        }