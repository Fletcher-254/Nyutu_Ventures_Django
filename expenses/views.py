from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from django.db.models.functions import TruncDate

@login_required
def daily_expense_report(request):
    """A high-level view for Directors to see daily spending totals."""
    if request.user.role.lower() not in ['director', 'manager']:
        return redirect('expense_list')

    # Groups expenses by date and sums the amounts
    daily_totals = (
        Expense.objects.filter(status='Approved')
        .annotate(day=TruncDate('date'))
        .values('day')
        .annotate(total=Sum('amount'))
        .order_by('-day')
    )

    return render(request, 'expenses/daily_report.html', {'daily_totals': daily_totals})

@login_required
def expense_list(request):
    """
    Displays the full list of expenses with optional filtering.
    Ordered by date (newest first).
    """
    status = request.GET.get('status')
    category = request.GET.get('category')
    
    # .order_by('-date') is critical for a professional list
    expenses = Expense.objects.all().order_by('-date')
    
    if status:
        expenses = expenses.filter(status=status)
    if category:
        expenses = expenses.filter(category=category)
        
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'current_status': status,
        'current_category': category
    })


@login_required
def expense_detail(request, pk):
    """Detailed view of a single expense claim."""
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})

@login_required
def expense_update(request, pk):
    """Allows editing if the expense is still pending."""
    expense = get_object_or_404(Expense, pk=pk)
    if expense.status != 'Pending':
        messages.error(request, "Approved or Rejected expenses cannot be edited.")
        return redirect('expense_detail', pk=pk)

    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Edit Expense Claim'})

@login_required
def expense_approve(request, pk):
    """Manager/Director action to approve or reject claims."""
    if request.user.role not in ['manager', 'director']:
        messages.error(request, "Unauthorized. Only managers can approve expenses.")
        return redirect('expense_list')

    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            expense.status = 'Approved'
        elif action == 'reject':
            expense.status = 'Rejected'
        
        expense.approved_by = request.user
        expense.save()
        messages.info(request, f"Expense has been {action}ed.")
        return redirect('expense_detail', pk=pk)
    
    return render(request, 'expenses/expense_approve.html', {'expense': expense})

@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.submitted_by = request.user  # Assign the logged-in user
            expense.save()
            messages.success(request, "Expense recorded and logged successfully.")
            return redirect('admin_dashboard') # or your expense list
    else:
        form = ExpenseForm()
    
    return render(request, 'expenses/expense_form.html', {'form': form})