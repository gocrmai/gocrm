from django.urls import path
from . import views

app_name = 'hardware'

urlpatterns = [
    # Computer
    path('computers/', views.computer_list, name='computer_list'),
    path('computers/new/', views.computer_create, name='computer_create'),
    path('computers/<int:pk>/edit/', views.computer_edit, name='computer_edit'),
    path('computers/<int:pk>/delete/', views.computer_delete, name='computer_delete'),
    
    # Printer
    path('printers/', views.printer_list, name='printer_list'),
    path('printers/new/', views.printer_create, name='printer_create'),
    path('printers/<int:pk>/edit/', views.printer_edit, name='printer_edit'),
    path('printers/<int:pk>/delete/', views.printer_delete, name='printer_delete'),
]