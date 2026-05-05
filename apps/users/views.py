from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden


def login_view(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, '您的帳戶已被停用。')
        else:
            messages.error(request, '用戶名或密碼錯誤。')

    return render(request, 'users/login.html')


def logout_view(request):
    """User logout."""
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """Main dashboard page."""
    from apps.tasks.models import Task
    from apps.customers.models import Customer

    # Get user's tasks
    if request.user.is_supervisor():
        tasks = Task.objects.all()
        customers = Customer.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user) | Task.objects.filter(created_by=request.user)
        customers = Customer.objects.filter(created_by=request.user)

    # Task statistics
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    completed_tasks = tasks.filter(status='completed').count()

    # Recent tasks
    recent_tasks = tasks.order_by('-created_at')[:10]

    context = {
        'total_customers': customers.count(),
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'recent_tasks': recent_tasks,
    }

    return render(request, 'users/dashboard.html', context)


@login_required
def my_tasks(request):
    """Show tasks assigned to or created by current user."""
    from apps.tasks.models import Task
    from django.db.models import Q
    
    tasks = Task.objects.filter(
        Q(assigned_to=request.user) | Q(created_by=request.user)
    ).distinct().order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(tasks, 20)
    page = request.GET.get('page', 1)
    tasks = paginator.get_page(page)

    return render(request, 'tasks/my_tasks.html', {
        'tasks': tasks,
        'status_filter': status_filter,
    })


def handler403(request, exception):
    """403 Forbidden handler."""
    return render(request, 'users/403.html', status=403)


def handler404(request, exception):
    """404 Not Found handler."""
    return render(request, 'users/404.html', status=404)


def handler500(request):
    """500 Server Error handler."""
    return render(request, 'users/500.html', status=500)