from django.urls import path
from .views import employee_list, employee_detail, daily_attendance,toggle_attendance,update_employee,delete_employee

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('<int:pk>/', employee_detail, name='employee_detail'),
    path('attendance/', daily_attendance, name='daily_attendance'),
    path('attendance/toggle/<int:employee_id>/', toggle_attendance, name='toggle_attendance'),
    path('<int:pk>/edit/', update_employee, name='update_employee'),
    path('<int:pk>/delete/', delete_employee, name='delete_employee'),
]
