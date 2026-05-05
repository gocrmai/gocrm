"""
Hardware views for GOPOS CRM.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Computer, Printer
from .forms import ComputerForm, PrinterForm
from apps.customers.models import Customer


@login_required
def computer_list(request):
    """List all computers with optional customer filter."""
    computers = Computer.objects.all()
    
    # Filter by customer
    customer_id = request.GET.get('customer', '')
    if customer_id:
        computers = computers.filter(customer_id=customer_id)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        computers = computers.filter(
            Q(customer__shop_name__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(hostname__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(computers, 20)
    page = request.GET.get('page', 1)
    computers = paginator.get_page(page)
    
    customers = Customer.objects.all()
    
    return render(request, 'hardware/computer_list.html', {
        'computers': computers,
        'customers': customers,
        'search_query': search_query,
    })


@login_required
def computer_create(request):
    """Create a new computer."""
    customer_id = request.GET.get('customer', '')
    initial = {}
    if customer_id:
        initial['customer'] = customer_id
    
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '電腦資料已創建。')
            return redirect('hardware:computer_list')
    else:
        form = ComputerForm(initial=initial)
    
    return render(request, 'hardware/computer_form.html', {
        'form': form,
        'title': '新增電腦',
    })


@login_required
def computer_edit(request, pk):
    """Edit a computer."""
    computer = get_object_or_404(Computer, pk=pk)
    
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            messages.success(request, '電腦資料已更新。')
            return redirect('hardware:computer_list')
    else:
        form = ComputerForm(instance=computer)
    
    return render(request, 'hardware/computer_form.html', {
        'form': form,
        'computer': computer,
        'title': '編輯電腦',
    })


@login_required
def computer_delete(request, pk):
    """Delete a computer."""
    computer = get_object_or_404(Computer, pk=pk)
    
    if request.method == 'POST':
        computer.delete()
        messages.success(request, '電腦資料已刪除。')
        return redirect('hardware:computer_list')
    
    return render(request, 'hardware/computer_delete.html', {
        'computer': computer,
    })


@login_required
def printer_list(request):
    """List all printers with optional customer filter."""
    printers = Printer.objects.all()
    
    customer_id = request.GET.get('customer', '')
    if customer_id:
        printers = printers.filter(customer_id=customer_id)
    
    search_query = request.GET.get('search', '')
    if search_query:
        printers = printers.filter(
            Q(customer__shop_name__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(name__icontains=search_query)
        )
    
    paginator = Paginator(printers, 20)
    page = request.GET.get('page', 1)
    printers = paginator.get_page(page)
    
    customers = Customer.objects.all()
    
    return render(request, 'hardware/printer_list.html', {
        'printers': printers,
        'customers': customers,
        'search_query': search_query,
    })


@login_required
def printer_create(request):
    """Create a new printer."""
    customer_id = request.GET.get('customer', '')
    initial = {}
    if customer_id:
        initial['customer'] = customer_id
    
    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '打印機資料已創建。')
            return redirect('hardware:printer_list')
    else:
        form = PrinterForm(initial=initial)
    
    return render(request, 'hardware/printer_form.html', {
        'form': form,
        'title': '新增打印機',
    })


@login_required
def printer_edit(request, pk):
    """Edit a printer."""
    printer = get_object_or_404(Printer, pk=pk)
    
    if request.method == 'POST':
        form = PrinterForm(request.POST, instance=printer)
        if form.is_valid():
            form.save()
            messages.success(request, '打印機資料已更新。')
            return redirect('hardware:printer_list')
    else:
        form = PrinterForm(instance=printer)
    
    return render(request, 'hardware/printer_form.html', {
        'form': form,
        'printer': printer,
        'title': '編輯打印機',
    })


@login_required
def printer_delete(request, pk):
    """Delete a printer."""
    printer = get_object_or_404(Printer, pk=pk)
    
    if request.method == 'POST':
        printer.delete()
        messages.success(request, '打印機資料已刪除。')
        return redirect('hardware:printer_list')
    
    return render(request, 'hardware/printer_delete.html', {
        'printer': printer,
    })