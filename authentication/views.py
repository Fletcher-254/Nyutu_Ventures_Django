from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, F
from django.contrib import messages

# Cleaned up imports - removed the stray 'E'
from employees.models import Employee, Attendance, EmployeeAccount
from expenses.models import Expense
from vendors.models import Vendor, VendorAccount
from .forms import LoginForm 

def login_view(request):
    if request.user.is_authenticated:
        role = getattr(request.user, 'role', '').lower()
        if role == 'admin':
            return redirect('admin_dashboard')
        return redirect('director_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                role = getattr(user, 'role', '').lower()
                if role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('director_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully. Secure session ended.")
    return redirect('login')

@login_required
def admin_dashboard(request):
    """The Operations Command Center."""
    today = timezone.now().date()
    
    total_staff = Employee.objects.filter(deleted_at__isnull=True).count()
    present_today = Attendance.objects.filter(date=today, is_present=True).count()
    daily_expense_total = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    recent_activity = Expense.objects.select_related('category').order_by('-id')[:5]

    context = {
        'total_staff': total_staff,
        'present_today': present_today,
        'daily_expense_total': daily_expense_total,
        'recent_activity': recent_activity,
        'daily_quote': "Efficiency is doing things right; effectiveness is doing the right things.",
        'now': timezone.now(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def director_dashboard(request):
    """The Executive Financial Oversight View."""
    account_stats = VendorAccount.objects.aggregate(
        actual_debt=Sum(F('total_owed') - F('total_paid'))
    )
    total_debt = account_stats['actual_debt'] or 0
    
    current_month = timezone.now().month
    monthly_spending = Expense.objects.filter(
        date__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    top_debt_vendors = VendorAccount.objects.annotate(
        debt_balance=F('total_owed') - F('total_paid')
    ).select_related('vendor').filter(debt_balance__gt=0).order_by('-debt_balance')[:5]

    context = {
        'total_debt': total_debt,
        'monthly_spending': monthly_spending,
        'top_debt_vendors': top_debt_vendors,
        'now': timezone.now(),
    }
    return render(request, 'dashboard/director_dashboard.html', context)

@login_required
def unpaid_bills_unified(request):
    # Vendor debt calculation
    vendor_debts = VendorAccount.objects.annotate(
        balance=F('total_owed') - F('total_paid')
    ).filter(balance__gt=0)
    total_vendor_debt = vendor_debts.aggregate(Sum('balance'))['balance__sum'] or 0

    # Employee debt calculation
    employee_debts = EmployeeAccount.objects.annotate(
        balance=F('total_earned') - F('total_paid')
    ).filter(balance__gt=0)
    total_employee_debt = employee_debts.aggregate(Sum('balance'))['balance__sum'] or 0

    total_liabilities = total_vendor_debt + total_employee_debt

    return render(request, 'finance/unpaid_bills.html', {
        'vendor_debts': vendor_debts,
        'employee_debts': employee_debts,
        'total_liabilities': total_liabilities
    })