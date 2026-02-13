from django.urls import path
# Import exactly what you have in your views.py
from .views import (
    employee_list, 
    employee_detail, 
    daily_attendance, 
    toggle_attendance, 
    update_employee, 
    delete_employee, 
    director_employee_payout_list, # Fixed name to match your views.py
    process_payment
)

urlpatterns = [
    # Main List & Detail
    path('', employee_list, name='employee_list'),
    path('<int:pk>/', employee_detail, name='employee_detail'),

    # Attendance Logic
    path('attendance/', daily_attendance, name='daily_attendance'),
    path('attendance/toggle/<int:employee_id>/', toggle_attendance, name='toggle_attendance'),

    # Management (Admin) - Using names that match your templates
    path('<int:pk>/edit/', update_employee, name='employee_update'),
    path('<int:pk>/delete/', delete_employee, name='employee_delete'),

    # Financial (Director/Manager)
    path('payouts/', director_employee_payout_list, name='director_employee_payout'),
    path('process-payment/<int:employee_id>/', process_payment, name='process_payment'),
]