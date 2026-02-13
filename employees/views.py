from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.contrib import messages

from .models import Employee, EmployeeHistory, Attendance
from .forms import EmployeeForm

@login_required
def employee_list(request):
    """Main workforce directory with daily payroll overhead tracking."""
    employees = Employee.objects.filter(deleted_at__isnull=True).order_by('-id')
    total_daily_salary = employees.aggregate(total=Sum('salary_per_day'))['total'] or 0
    
    if request.method == "POST":
        if request.user.role.lower() == 'director':
            return HttpResponseForbidden("Access Denied: Directors cannot register staff.")

        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            # Log the registration
            EmployeeHistory.objects.create(
                employee=employee,
                user=request.user,
                action="Registered",
                changes="Initial registration"
            )
            messages.success(request, f"Corporate record created for {employee.name}")
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/list.html', {
        'employees': employees, 
        'form': form, 
        'total_daily_salary': total_daily_salary
    })

@login_required
def employee_detail(request, pk):
    """Detailed profile including current month's payroll accrual and history."""
    employee = get_object_or_404(Employee, pk=pk)
    today = timezone.now()
    
    # Calculate monthly payroll data (based on actual presence)
    attendances = Attendance.objects.filter(
        employee=employee, 
        is_present=True,
        date__month=today.month,
        date__year=today.year
    )
    
    attendance_count = attendances.count()
    total_due = attendance_count * employee.salary_per_day
    history = employee.history.all().order_by('-timestamp')
    
    context = {
        'employee': employee,
        'attendance_count': attendance_count,
        'total_due': total_due,
        'history': history,
        'present_days': [a.date.day for a in attendances]
    }
    return render(request, 'employees/detail.html', context)

@login_required
def daily_attendance(request):
    """The Roll Call Interface. Restricted to Admin/Manager roles."""
    if request.user.role.lower() == 'director':
        messages.warning(request, "Financial oversight accounts do not have Roll Call permissions.")
        return redirect('employee_list')

    today = timezone.now().date()
    # Active staff only
    employees = Employee.objects.filter(deleted_at__isnull=True)
    
    # Get IDs of staff already marked present today for the UI state
    present_ids = Attendance.objects.filter(
        date=today, 
        is_present=True
    ).values_list('employee_id', flat=True)

    return render(request, 'employees/attendance_sheet.html', {
        'employees': employees,
        'today': today,
        'present_ids': present_ids
    })

@login_required
def toggle_attendance(request, employee_id):
    """AJAX-ready toggle to flip attendance status without page refresh."""
    if request.user.role.lower() == 'director':
        return HttpResponseForbidden("Unauthorized: Action restricted to Operations.")

    if request.method == "POST":
        today = timezone.now().date()
        employee = get_object_or_404(Employee, id=employee_id)
        
        attendance, created = Attendance.objects.get_or_create(
            employee=employee, 
            date=today
        )
        
        attendance.is_present = not attendance.is_present
        attendance.save()

        # Return a partial HTML for the button (HTMX/AJAX style)
        return render(request, 'employees/partials/attendance_button.html', {
            'employee': employee,
            'is_present': attendance.is_present
        })

@login_required
def update_employee(request, pk):
    """Edit staff details with automated change logging."""
    if request.user.role.lower() == 'director':
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        # Store old values for comparison
        old_name = employee.name
        old_phone = employee.phone
        old_salary = employee.salary_per_day
        
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save()
            
            # Log specific changes for accountability
            changes = []
            if old_name != employee.name: changes.append(f"Name change")
            if old_phone != employee.phone: changes.append(f"Phone updated")
            if old_salary != employee.salary_per_day: changes.append(f"Salary adjustment: {old_salary} to {employee.salary_per_day}")
            
            EmployeeHistory.objects.create(
                employee=employee,
                user=request.user,
                action="Updated",
                changes=", ".join(changes) if changes else "Profile refreshed"
            )
            messages.success(request, "Employee profile updated.")
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employees/employee_form_edit.html', {'form': form, 'employee': employee})

@login_required
def delete_employee(request, pk):
    """Professional Soft Delete (Archiving) instead of hard database deletion."""
    if request.user.role.lower() == 'director':
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=pk)
    employee.deleted_at = timezone.now()
    employee.save()

    EmployeeHistory.objects.create(
        employee=employee,
        user=request.user,
        action="Archived",
        changes="Record moved to soft-delete storage."
    )
    messages.info(request, f"Record for {employee.name} has been archived.")
    return redirect('employee_list')