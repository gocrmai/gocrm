"""
Task views for GOPOS CRM.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from io import BytesIO

from .models import Task
from .forms import TaskForm
from apps.users.models import User


@login_required
def task_list(request):
    """List all tasks with filtering."""
    tasks = Task.objects.all()

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    # Filter by assigned user
    assigned_filter = request.GET.get('assigned', '')
    if assigned_filter:
        tasks = tasks.filter(assigned_to__id=assigned_filter)

    # My tasks filter
    my_tasks = request.GET.get('my_tasks', '')
    if my_tasks:
        tasks = tasks.filter(assigned_to=request.user) | tasks.filter(created_by=request.user)

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(
            Q(task_number__icontains=search_query) |
            Q(customer__shop_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(tasks, 20)
    page = request.GET.get('page', 1)
    tasks = paginator.get_page(page)

    # Get all users for filter dropdown
    users = User.objects.filter(is_active=True)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'users': users,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'assigned_filter': assigned_filter,
    })


@login_required
def my_tasks(request):
    """Show tasks assigned to or created by current user."""
    tasks = Task.objects.filter(
        Q(assigned_to=request.user) | Q(created_by=request.user)
    ).distinct().order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    paginator = Paginator(tasks, 20)
    page = request.GET.get('page', 1)
    tasks = paginator.get_page(page)

    return render(request, 'tasks/my_tasks.html', {
        'tasks': tasks,
        'status_filter': status_filter,
    })


@login_required
def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Save many-to-many relationships

            # Send notification to assigned users
            if task.assigned_to.exists():
                messages.success(request, f'任務「{task.task_number}」已創建並指派。')
            else:
                messages.success(request, f'任務「{task.task_number}」已創建。')

            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': '新建任務',
    })


@login_required
def task_detail(request, pk):
    """View task details."""
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {
        'task': task,
    })


@login_required
def task_edit(request, pk):
    """Edit a task."""
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'任務「{task.task_number}」已更新。')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task,
        'title': '編輯任務',
    })


@login_required
def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task_number = task.task_number
        task.delete()
        messages.success(request, f'任務「{task_number}」已刪除。')
        return redirect('task_list')

    return render(request, 'tasks/task_delete.html', {
        'task': task,
    })


@login_required
def task_receive(request, pk):
    """Mark task as received by user."""
    task = get_object_or_404(Task, pk=pk)

    if request.user in task.assigned_to.all():
        if task.status == 'pending':
            task.status = 'received'
            task.save()
            messages.success(request, f'任務「{task.task_number}」已接收。')
        else:
            messages.warning(request, f'任務「{task.task_number}」狀態不是待處理。')
    else:
        messages.error(request, '您不是此任務的被指派人。')

    return redirect('task_detail', pk=task.pk)


@login_required
def task_complete(request, pk):
    """Mark task as completed."""
    task = get_object_or_404(Task, pk=pk)

    if request.user in list(task.assigned_to.all()) or request.user.is_supervisor():
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        messages.success(request, f'任務「{task.task_number}」已完成。')
    else:
        messages.error(request, '您沒有權限完成此任務。')

    return redirect('task_detail', pk=task.pk)


@login_required
def task_print(request, pk):
    """Generate printable worksheet (維修單) for a task."""
    task = get_object_or_404(Task, pk=pk)

    # Render HTML for PDF
    html = render_to_string('tasks/task_print.html', {
        'task': task,
        'company_name_c': '創域科技有限公司',
        'company_name_e': 'Join Witt Technology System Limited',
        'company_address': '九龍觀塘開源道55號開聯工業中心A座11樓17室',
        'company_tel': '2488 2338',
        'company_fax': '2488 2308',
        'company_email': 'cs@gopos.hk',
    })

    # For now, return HTML response for printing
    return HttpResponse(html)