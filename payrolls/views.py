from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employees.models import Employee, Attendance
from django.db.models import Count, Q

@login_required
def master_payroll(request):
    # Only Director and Project Manager can see this
    if request.user.role not in ['director', 'manager']:
        return render(request, '403.html', status=403)

    # Fetch employees and count their present days for the current month
    # We use 'annotate' to do the math in the database (very efficient)
    employees = Employee.objects.annotate(
        days_present=Count('attendances', filter=Q(attendances__is_present=True))
    )

    payroll_data = []
    total_payroll_due = 0

    for emp in employees:
        due = emp.days_present * emp.salary_per_day
        total_payroll_due += due
        payroll_data.append({
            'name': emp.name,
            'days': emp.days_present,
            'rate': emp.salary_per_day,
            'total': due
        })

    return render(request, 'payrolls/master_list.html', {
        'payroll_data': payroll_data,
        'grand_total': total_payroll_due
    })
