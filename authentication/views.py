from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages

# Import models from your other apps
from employees.models import Employee, Attendance
from expenses.models import Expense
from vendors.models import Vendor, VendorAccount
from .forms import LoginForm 

def login_view(request):
    """The gateway: Redirects users based on their role after login."""
    if request.user.is_authenticated:
        if request.user.role.lower() == 'admin':
            return redirect('admin_dashboard')
        return redirect('director_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.role.lower() == 'admin':
                    return redirect('admin_dashboard')
                return redirect('director_dashboard')
            else:
                messages.error(request, "Invalid corporate credentials.")
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    """The Operations Command Center."""
    today = timezone.now().date()
    
    # Staff Stats: Live data for the 'Staff Present' card
    total_staff = Employee.objects.filter(deleted_at__isnull=True).count()
    present_today = Attendance.objects.filter(date=today, is_present=True).count()
    
    # Financial Stats: Real-time KES outflow today
    daily_expense_total = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent Activity: Feeds the activity list
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
    # Total Company Debt: Feeds the 'Total Outstanding' card
    total_debt = VendorAccount.objects.aggregate(Sum('current_balance'))['current_balance__sum'] or 0
    
    # Monthly Spending: Performance tracking
    current_month = timezone.now().month
    monthly_spending = Expense.objects.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Priority Debts: Feeds the list of vendors that need immediate payment
    top_debt_vendors = VendorAccount.objects.select_related('vendor').order_by('-current_balance')[:5]

    context = {
        'total_debt': total_debt,
        'monthly_spending': monthly_spending,
        'top_debt_vendors': top_debt_vendors,
        'now': timezone.now(),
    }
    return render(request, 'dashboard/director_dashboard.html', context)