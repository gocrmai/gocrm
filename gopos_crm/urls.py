"""
URL configuration for GOPOS CRM project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from reports.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('customers/', include('apps.customers.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('hardware/', include('apps.hardware.urls')),
    path('reports/', include('reports.urls')),
    path('reports/dashboard/', DashboardView.as_view(), name='reports_dashboard'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)