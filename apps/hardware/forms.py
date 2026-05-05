from django import forms
from .models import Computer, Printer


class ComputerForm(forms.ModelForm):
    """Form for creating and editing computers."""

    class Meta:
        model = Computer
        fields = ['customer', 'model', 'hostname', 'serial_number', 
                  'rustdesk_id', 'anydesk_id', 'warranty_expiry', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '設備型號'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '電腦名稱/主機名'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '序號'}),
            'rustdesk_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rustdesk ID'}),
            'anydesk_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Anydesk ID'}),
            'warranty_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '備註'}),
        }


class PrinterForm(forms.ModelForm):
    """Form for creating and editing printers."""

    class Meta:
        model = Printer
        fields = ['customer', 'model', 'name', 'ip_address', 'serial_number', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '打印機型號'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '名稱（如：廚房打印機）'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IP 地址'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '序號'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '備註'}),
        }