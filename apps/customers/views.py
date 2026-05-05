"""
Customer views for GOPOS CRM.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    """List all customers."""
    customers = Customer.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(shop_name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(customers, 20)  # 20 per page
    page = request.GET.get('page', 1)
    customers = paginator.get_page(page)

    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'search_query': search_query,
    })


@login_required
def customer_create(request):
    """Create a new customer."""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            messages.success(request, f'客戶「{customer.shop_name}」已創建。')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': '新增客戶',
    })


@login_required
def customer_detail(request, pk):
    """View customer details with related tasks and hardware."""
    customer = get_object_or_404(Customer, pk=pk)

    # Get related tasks
    tasks = customer.tasks.all()[:10]

    # Get related hardware
    hardware = customer.get_hardware()

    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'tasks': tasks,
        'computers': hardware['computers'],
        'printers': hardware['printers'],
    })


@login_required
def customer_edit(request, pk):
    """Edit a customer."""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'客戶「{customer.shop_name}」已更新。')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'customer': customer,
        'title': '編輯客戶',
    })


@login_required
def customer_delete(request, pk):
    """Delete a customer."""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        shop_name = customer.shop_name
        customer.delete()
        messages.success(request, f'客戶「{shop_name}」已刪除。')
        return redirect('customer_list')

    return render(request, 'customers/customer_delete.html', {
        'customer': customer,
    })